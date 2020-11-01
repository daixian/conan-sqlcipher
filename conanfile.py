from conans import tools, ConanFile, AutoToolsBuildEnvironment, RunEnvironment
import platform
import sys
import os


class SqlcipherConan(ConanFile):
    name = "sqlcipher"
    version = "4.3.0"
    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.zetetic.net/sqlcipher/"
    description = "SQLite extension that provides 256 bit AES encryption of database files."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [
        True, False], "crypto_library": ["openssl", "libressl"]}
    default_options = {"shared": False,
                       "fPIC": True, "crypto_library": "openssl"}
    topics = ("database", "encryption", "SQLite")
    exports_sources = "patches/*"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        self.build_requires("tcl/8.6.10")

    def requirements(self):
        if self.options.crypto_library == "openssl":
            # 这里不能使用它原先设置的新版本 https://github.com/conan-io/conan-center-index/pull/1380
            # 换用了1.0.2t构建成功
            self.requires("openssl/1.1.1h")
        else:
            self.requires("libressl/2.9.2")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _build_visual(self):
        crypto_dep = self.deps_cpp_info[str(self.options.crypto_library)]
        crypto_incdir = crypto_dep.include_paths[0]
        crypto_libdir = crypto_dep.lib_paths[0]
        crypto_dep.libs.append("user32")  # 解决windows平台上openssl的链接错误
        crypto_dep.libs.append("Advapi32")
        libs = map(lambda lib: lib + ".lib", crypto_dep.libs)

        nmake_flags = [
            "TLIBS=\"%s\"" % " ".join(libs),
            "LTLIBPATHS=/LIBPATH:%s" % crypto_libdir,
            "OPTS=\"-I%s -DSQLITE_HAS_CODEC \
-DSQLITE_DQS=0 \
-DSQLITE_MAX_ATTACHED=10 \
-DSQLITE_ENABLE_EXPLAIN_COMMENTS \
-DSQLITE_SOUNDEX \
-DSQLITE_ENABLE_COLUMN_METADATA \
-DSQLITE_SECURE_DELETE \
-DSQLITE_ENABLE_FTS3 \
-DSQLITE_ENABLE_FTS3_PARENTHESIS \
-DSQLITE_ENABLE_FTS4 \
-DSQLITE_ENABLE_FTS5 \
-DSQLITE_ENABLE_JSON1 \
-DSQLITE_ENABLE_RTREE \
-DSQLITE_ENABLE_GEOPOLY \
-DSQLITE_CORE \
-DSQLITE_ENABLE_EXTFUNC \
-DSQLITE_ENABLE_CSV \
-DSQLITE_ENABLE_SHA3 \
-DSQLITE_ENABLE_CARRAY \
-DSQLITE_ENABLE_FILEIO \
-DSQLITE_ENABLE_SERIES \
-DSQLITE_ENABLE_UUID \
-DSQLITE_TEMP_STORE=2 \
-DSQLITE_USE_URI \
\"" % (crypto_incdir),
            # -DSQLITE_USER_AUTHENTICATION \ 暂时不能加
            "NO_TCL=1",
            "USE_AMALGAMATION=1",
            'OPT_FEATURE_FLAGS="-DSQLCIPHER_CRYPTO_OPENSSL"',
            "TCLSH_CMD=%s" % self.deps_env_info.TCLSH,
        ]

        main_target = "dll" if self.options.shared else "sqlcipher.lib"

        if self.settings.compiler.runtime in ["MD", "MDd"]:
            nmake_flags.append("USE_CRT_DLL=1")
        # 这里正确的设置应该为0,但是可能由于openssl库的问题
        if self.settings.compiler.runtime in ["MT", "MTd"]:
            nmake_flags.append("USE_CRT_DLL=0")
        if self.settings.build_type == "Debug":
            nmake_flags.append("DEBUG=2")
        nmake_flags.append("FOR_WIN10=1")
        platforms = {"x86": "x86", "x86_64": "x64"}
        nmake_flags.append("PLATFORM=%s" % platforms[self.settings.arch.value])
        vcvars = tools.vcvars_command(self.settings)
        self.run("%s && nmake /f Makefile.msc %s %s" % (vcvars,
                                                        main_target, " ".join(nmake_flags)), cwd=self._source_subfolder)

    def _build_autotools(self):
        self.run('chmod +x configure', cwd=self._source_subfolder)
        absolute_install_dir = os.path.abspath(os.path.join(".", "install"))
        absolute_install_dir = absolute_install_dir.replace("\\", "/")
        autotools_env = AutoToolsBuildEnvironment(
            self, win_bash=tools.os_info.is_windows)
        if self.settings.os == "Linux":
            autotools_env.libs.append("dl")
        autotools_env.defines.extend(
            ["SQLITE_HAS_CODEC", "SQLCIPHER_CRYPTO_OPENSSL",
             "SQLITE_DQS=0",
             "SQLITE_MAX_ATTACHED=10",
             "SQLITE_ENABLE_EXPLAIN_COMMENTS",
             "SQLITE_SOUNDEX",
             "SQLITE_ENABLE_COLUMN_METADATA",
             "SQLITE_SECURE_DELETE",
             "SQLITE_ENABLE_FTS3",
             "SQLITE_ENABLE_FTS3_PARENTHESIS",
             "SQLITE_ENABLE_FTS4",
             "SQLITE_ENABLE_FTS5",
             "SQLITE_ENABLE_JSON1",
             "SQLITE_ENABLE_RTREE",
             "SQLITE_ENABLE_GEOPOLY",
             "SQLITE_CORE",
             "SQLITE_ENABLE_EXTFUNC",
             "SQLITE_ENABLE_CSV",
             "SQLITE_ENABLE_SHA3",
             "SQLITE_ENABLE_CARRAY",
             "SQLITE_ENABLE_FILEIO",
             "SQLITE_ENABLE_SERIES",
             "SQLITE_ENABLE_UUID",
             "SQLITE_TEMP_STORE=2",
             "SQLITE_USE_URI"])
        # "SQLITE_USER_AUTHENTICATION" 不能使用

        # sqlcipher config.sub does not contain android configurations...
        # elf is the most basic `os' for Android
        host = None
        if self.settings.os == "Android":
            host = "%s-linux-elf" % self.arch_id_str_compiler
        elif self.settings.os == "Windows":
            arch = str(self.settings.arch)
            if arch == "x86":
                arch = "i386"
            host = "%s-pc-mingw32" % arch
        elif self.settings.os == "iOS":
            host = "%s-apple-darwin" % self.settings.arch

        configure_args = self._get_configure_args(absolute_install_dir)
        with tools.chdir(self._source_subfolder):
            # Hack, uname -p returns i386, configure guesses x86_64, we must force i386 so that cross-compilation is correctly detected.
            # Otherwise host/build are the same, and configure tries to launch a sample executable, and fails miserably.
            env_vars = autotools_env.vars
            if self.settings.os == "iOS":
                build = "i386-apple-darwin"
            # same for mingw...
            elif self.settings.os == "Windows":
                build = "x86_64-linux"
                env_vars["config_TARGET_EXEEXT"] = ".exe"
            else:
                build = None
            autotools_env.configure(
                args=configure_args, host=host, build=build, vars=env_vars)
            if self.settings.os == "Windows":
                # sqlcipher will create .exe for the build machine, which is Linux...
                tools.replace_in_file(os.path.join(
                    self.build_folder, self._source_subfolder, "Makefile"), "BEXE = .exe", "BEXE = ")
            autotools_env.make(args=["install"])

    @property
    def _arch_id_str_compiler(self):
        return {"x86": "i686",
                "armv6": "arm",
                "armv7": "arm",
                "armv7hf": "arm",
                # Hack: config.guess of sqlcipher does not like aarch64
                "armv8": "armv8",
                "mips64": "mips64"}.get(str(self.settings.arch),
                                        str(self.settings.arch))

    def _get_configure_args(self, absolute_install_dir):
        args = [
            "--prefix=%s" % absolute_install_dir,

            self._autotools_bool_arg("shared", self.options.shared),
            self._autotools_bool_arg("static", not self.options.shared),
            "--enable-tempstore=yes",
            "--with-tcl={}".format(os.path.join(self.deps_env_info.TCL_ROOT, "lib"))
        ]
        if self.settings.os == "Windows":
            args.extend(["config_BUILD_EXEEXT='.exe'",
                         "config_TARGET_EXEEXT='.exe'"])
        return args

    def _autotools_bool_arg(self, arg_base_name, value):
        prefix = "--enable-" if value else "--disable-"

        return prefix + arg_base_name

    def build(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)
        if self.settings.os == "Macos":
            tools.replace_in_file(os.path.join(
                self._source_subfolder, "configure"), r"-install_name \$rpath/", "-install_name ")

        if self.settings.compiler == "Visual Studio":
            self._build_visual()
        else:
            self._build_autotools()

    def _package_unix(self):
        self.copy("*sqlite3.h", src="install")
        self.copy("*.so*", dst="lib", src="install",
                  keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", src="install", keep_path=False)
        self.copy("*.lib", dst="lib", src="install", keep_path=False)
        self.copy("*.dll", dst="bin", src="install", keep_path=False)
        self.copy("*.dylib", dst="lib", src="install", keep_path=False)
        self.copy("*LICENSE", dst="licenses", keep_path=False)

    def _package_visual(self):
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*LICENSE", dst="licenses", keep_path=False)
        self.copy("sqlite3.h", src=self._source_subfolder,
                  dst=os.path.join("include", "sqlcipher"))

    def package(self):
        if self.settings.compiler == "Visual Studio":
            self._package_visual()
        else:
            self._package_unix()

    def package_info(self):
        self.cpp_info.libs = ["sqlcipher"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("user32")
            self.cpp_info.libs.append("Advapi32")
        if self.settings.os == "Linux":
            # 在 arm上编译增加m库可以静态的编译成功,但目前shared的还不能成功
            self.cpp_info.system_libs.extend(["pthread", "dl", "m"])

        self.cpp_info.defines = ["SQLITE_HAS_CODEC",
                                 'SQLCIPHER_CRYPTO_OPENSSL',
                                 "SQLITE_DQS=0",
                                 "SQLITE_MAX_ATTACHED=10",
                                 "SQLITE_ENABLE_EXPLAIN_COMMENTS",
                                 "SQLITE_SOUNDEX",
                                 "SQLITE_ENABLE_COLUMN_METADATA",
                                 "SQLITE_SECURE_DELETE",
                                 "SQLITE_ENABLE_FTS3",
                                 "SQLITE_ENABLE_FTS3_PARENTHESIS",
                                 "SQLITE_ENABLE_FTS4",
                                 "SQLITE_ENABLE_FTS5",
                                 "SQLITE_ENABLE_JSON1",
                                 "SQLITE_ENABLE_RTREE",
                                 "SQLITE_ENABLE_GEOPOLY",
                                 "SQLITE_CORE",
                                 "SQLITE_ENABLE_EXTFUNC",
                                 "SQLITE_ENABLE_CSV",
                                 "SQLITE_ENABLE_SHA3",
                                 "SQLITE_ENABLE_CARRAY",
                                 "SQLITE_ENABLE_FILEIO",
                                 "SQLITE_ENABLE_SERIES",
                                 "SQLITE_ENABLE_UUID",
                                 "SQLITE_TEMP_STORE=2",
                                 "SQLITE_USE_URI"]
        # Allow using #include <sqlite3.h> even with sqlcipher (for libs like sqlpp11-connector-sqlite3)
        self.cpp_info.includedirs.append(os.path.join("include", "sqlcipher"))
