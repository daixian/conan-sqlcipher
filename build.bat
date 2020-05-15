chcp 65001
REM windows平台编译项目
set CONAN_REVISIONS_ENABLED=1
conan create . daixian/stable -s build_type=Release --build missing -o sqlcipher:shared=False
conan create . daixian/stable -s build_type=Release --build missing -o sqlcipher:shared=True
REM conan create . daixian/stable -s compiler.version=16 -s compiler.runtime=MD -s arch=x86_64 -s build_type=Release --build missing
REM conan upload cvsystem/3.0.1@daixian/stable --all -r=conan-local

REM mkdir build
REM cd build
REM mkdir Win64
REM cd Win64
REM cmake.exe -G "Visual Studio 15 2017 Win64" "../../" -DBUILD_GMOCK:BOOL="0" -DINSTALL_GTEST:BOOL="0" -Dgtest_force_shared_crt:BOOL="1" -DBUILD_TESTING:BOOL="0" -DENABLE_TEST:BOOL="1" -DCMAKE_CONFIGURATION_TYPES:STRING="Release;RelWithDebInfo"