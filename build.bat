chcp 65001
REM windows平台编译项目
set CONAN_REVISIONS_ENABLED=1

conan create . daixian/stable -s arch=x86_64 -s compiler.runtime=MD -s build_type=Release --build missing -o sqlcipher:shared=True
conan create . daixian/stable -s arch=x86_64 -s compiler.runtime=MT -s build_type=Release --build missing -o sqlcipher:shared=True
conan create . daixian/stable -s arch=x86 -s compiler.runtime=MD -s build_type=Release --build missing -o sqlcipher:shared=True
conan create . daixian/stable -s arch=x86 -s compiler.runtime=MT -s build_type=Release --build missing -o sqlcipher:shared=True

conan create . daixian/stable -s arch=x86_64 -s compiler.runtime=MD -s build_type=Release --build missing -o sqlcipher:shared=False
conan create . daixian/stable -s arch=x86_64 -s compiler.runtime=MT -s build_type=Release --build missing -o sqlcipher:shared=False
conan create . daixian/stable -s arch=x86 -s compiler.runtime=MD -s build_type=Release --build missing -o sqlcipher:shared=False
conan create . daixian/stable -s arch=x86 -s compiler.runtime=MT -s build_type=Release --build missing -o sqlcipher:shared=False

@REM conan create . daixian/stable -s compiler.runtime=MT -s build_type=Release --build openssl --build sqlcipher -o sqlcipher:shared=True
REM conan create . daixian/stable -s compiler.version=16 -s compiler.runtime=MD -s arch=x86_64 -s build_type=Release --build missing
REM conan upload sqlcipher/4.3.0@daixian/stable --all -r=conan-local