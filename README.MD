# 记录
## 构建
1. OpenSSL库的版本
只有某些版本的构建脚本能够成功.目前只能使用openssl/1.0.2t.如果设置openssl/1.1.1g,windows平台错误如下：
    ``` yml
    libcrypto.lib(cryptlib.obj) : error LNK2019: unresolved external symbol __imp_RegisterEventSourceW referenced in function OPENSSL_showfatal
    libcrypto.lib(cryptlib.obj) : error LNK2019: unresolved external symbol __imp_ReportEventW referenced in function OPENSSL_showfatal
    libcrypto.lib(cryptlib.obj) : error LNK2019: unresolved external symbol __imp_GetProcessWindowStation referenced in function OPENSSL_isservice
    libcrypto.lib(cryptlib.obj) : error LNK2019: unresolved external symbol __imp_GetUserObjectInformationW referenced in function OPENSSL_isservice
    libcrypto.lib(cryptlib.obj) : error LNK2019: unresolved external symbol __imp_MessageBoxW referenced in function OPENSSL_showfatal
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptAcquireContextW referenced in function capi_ctx_set_provname
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptReleaseContext referenced in function capi_ctx_set_provname
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptDestroyKey referenced in function capi_dsa_free
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptSetHashParam referenced in function capi_dsa_do_sign
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptGetProvParam referenced in function capi_list_containers
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptGetUserKey referenced in function capi_get_key
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptExportKey referenced in function capi_get_pkey
    libcrypto.lib(e_aes_cbc_hmac_sha256.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(e_aes_cbc_hmac_sha256.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptDecrypt referenced in function capi_rsa_priv_dec
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptCreateHash referenced in function capi_dsa_do_sign
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptDestroyHash referenced in function capi_dsa_do_sign
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptSignHashW referenced in function capi_dsa_do_sign
    libcrypto.lib(e_capi.obj) : error LNK2019: unresolved external symbol __imp_CryptEnumProvidersW referenced in function capi_get_provname
    libcrypto.lib(e_aria.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(e_aria.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    libcrypto.lib(e_camellia.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(e_camellia.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    libcrypto.lib(e_chacha20_poly1305.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(e_chacha20_poly1305.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    libcrypto.lib(e_seed.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(e_seed.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    libcrypto.lib(e_sm4.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(e_sm4.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    sqlcipher.dll : fatal error LNK1120: 18 unresolved externals
    libcrypto.lib(m_md4.obj) : warning LNK4099: PDB 'ossl_static.pdb' was not found with 'libcrypto.lib(m_md4.obj)' or at 'C:\Users\dx\.conan\data\sqlcipher\4.3.0\daixian\stable\build\eafbb4d87ba1f1d584ee5a271903d949de437aaf\source_subfolder\ossl_static.pdb'; linking object as if no debug info
    NMAKE : fatal error U1077: '"C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Tools\MSVC\14.25.28610\bin\HostX64\x64\link.exe"' : return code '0x460'
    Stop.
    ```
    另外,这些OpenSSL构建脚本在arm的linux上以shared=False来构建都会有链接错误.几个SHA函数符号重定义错误.初步怀疑是openssl构建脚本的问题.
    通过添加 
    ``` python    
    crypto_dep.libs.append("user32") # 解决windows平台上openssl的链接错误
    crypto_dep.libs.append("Advapi32")
    ```
* SQLite3的./autoconf/Makefile.msc里定义的DEFAULTLIB有问题,会导致MT链接的时候出错,可以看到实际的DEFAULTLIB错了
    * 微软的CRT文档 https://docs.microsoft.com/en-us/cpp/c-runtime-library/crt-library-features?view=msvc-160
```
link.exe /DEBUG   /NOLOGO /MACHINE:x64 /DYNAMICBASE mincore.lib /guard:cf "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\lib\10.0.19041.0\ucrt\x64" /NODEFAULTLIB:libucrtd.lib /DEFAULTLIB:ucrtd.lib /LIBPATH:C:\Users\dx\.conan\data\openssl\1.1.1h\_\_\package\a79a557254fabcb77849dd623fed97c9c5ab7651\lib /DLL  /OUT:sqlcipher.dll sqlite3.lo sqlite3res.lo  libssl.lib libcrypto.lib user32.lib Advapi32.lib
```
原本的./autoconf/Makefile.msc文件如下
``` Makefile
!IF $(FOR_WIN10)!=0
LTLINKOPTS = $(LTLINKOPTS) /guard:cf "/LIBPATH:$(UCRTLIBPATH)"
!IF $(DEBUG)>1
LTLINKOPTS = $(LTLINKOPTS) /NODEFAULTLIB:libucrtd.lib /DEFAULTLIB:ucrtd.lib
!ELSE
LTLINKOPTS = $(LTLINKOPTS) /NODEFAULTLIB:libucrt.lib /DEFAULTLIB:ucrt.lib
!ENDIF
!ENDIF
```
利用 USE_CRT_DLL 来修改,MT的时候USE_CRT_DLL=0;
``` Makefile
!IF $(FOR_WIN10)!=0
LTLINKOPTS = $(LTLINKOPTS) /guard:cf "/LIBPATH:$(UCRTLIBPATH)"
# USE_CRT_DLL!=0 is MD
!IF $(USE_CRT_DLL)!=0
	!IF $(DEBUG)>1
	LTLINKOPTS = $(LTLINKOPTS) /NODEFAULTLIB:libucrtd.lib /DEFAULTLIB:ucrtd.lib
	!ELSE
	LTLINKOPTS = $(LTLINKOPTS) /NODEFAULTLIB:libucrt.lib /DEFAULTLIB:ucrt.lib
	!ENDIF
!ELSE # MT
	!IF $(DEBUG)>1
	LTLINKOPTS = $(LTLINKOPTS) /NODEFAULTLIB:ucrtd.lib /DEFAULTLIB:libucrtd.lib
	!ELSE
	LTLINKOPTS = $(LTLINKOPTS) /NODEFAULTLIB:ucrt.lib /DEFAULTLIB:libucrt.lib
	!ENDIF
!ENDIF	
!ENDIF
```
这里实际上可以不用修改,保持原样就可以了,只有带d和不带d会引起error.去掉补丁中那人的改动

* 这个是def文件的生成方法,使用dumpbin
``` Makefile
 # <<block2>>
-sqlite3.def:	libsqlite3.lib
-	echo EXPORTS > sqlite3.def
-	dumpbin /all libsqlite3.lib \
+sqlcipher.def:	sqlcipher.lib
+	echo EXPORTS > sqlcipher.def
+	dumpbin /all sqlcipher.lib \
 		| $(TCLSH_CMD) $(TOP)\tool\replace.tcl include "^\s+1 _?(sqlite3(?:session|changeset|changegroup|rebaser)?_[^@]*)(?:@\d+)?$$" \1 \
 		| sort >> sqlite3.def
 # <</block2>>
```

2. arm上加SQLITE_USER_AUTHENTICATION的宏定义也会提示找不到文件.

## 测试
* 加密数据库的执行时间，一条数据4MB大小
    ``` log
    [----------] 1 test from DBCommon
    [ RUN      ] DBCommon.creatNewDB
    Active code page: 65001
    [I][200518 17:22:45.411 37424] dlog移除过早的日志文件C:\Users\dx\AppData\Roaming\log\dlog.20200513-154052.log
    [I][200518 17:22:45.412 37424] 插入一条新数据dev_id
    [I][200518 17:22:45.422 37424] 插入一条新数据dev_id2
    [I][200518 17:22:45.431 37424] 插入一条新数据dev_id3
    [I][200518 17:22:45.442 37424] DBCommon.writeToDB():选中了项id=3,更新它的数据...
    [I][200518 17:22:45.471 37424] DBCommon.readOne():选中了项id=3
    [I][200518 17:22:45.495 37424] DBCommon.closeDB():关闭了数据库!
    [       OK ] DBCommon.creatNewDB (204 ms)
    [----------] 1 test from DBCommon (209 ms total)
    ```
* 数据库不加密，时间基本相同
    ``` log
    [----------] 1 test from DBCommon
    [ RUN      ] DBCommon.creatNewDB
    Active code page: 65001
    [I][200518 17:22:02.154 6200] dlog移除过早的日志文件C:\Users\dx\AppData\Roaming\log\dlog.20200513-153947.log
    [I][200518 17:22:02.155 6200] 插入一条新数据dev_id
    [I][200518 17:22:02.166 6200] 插入一条新数据dev_id2
    [I][200518 17:22:02.177 6200] 插入一条新数据dev_id3
    [I][200518 17:22:02.188 6200] DBCommon.writeToDB():选中了项id=3,更新它的数据...
    [I][200518 17:22:02.217 6200] DBCommon.readOne():选中了项id=3
    [I][200518 17:22:02.241 6200] DBCommon.closeDB():关闭了数据库!
    [       OK ] DBCommon.creatNewDB (196 ms)
    [----------] 1 test from DBCommon (197 ms total)
    ```
* 把一条数据改成16MB大小，那么时间会更长
    ``` log
    [----------] 1 test from DBCommon
    [ RUN      ] DBCommon.creatNewDB
    Active code page: 65001
    [I][200518 17:20:48.535 34948] dlog移除过早的日志文件C:\Users\dx\AppData\Roaming\log\dlog.20200513-153921.log
    [I][200518 17:20:48.536 34948] 插入一条新数据dev_id
    [I][200518 17:20:48.572 34948] 插入一条新数据dev_id2
    [I][200518 17:20:48.609 34948] 插入一条新数据dev_id3
    [I][200518 17:20:48.649 34948] DBCommon.writeToDB():选中了项id=3,更新它的数据...
    [I][200518 17:20:48.760 34948] DBCommon.readOne():选中了项id=3
    [I][200518 17:20:48.851 34948] DBCommon.closeDB():关闭了数据库!
    [       OK ] DBCommon.creatNewDB (453 ms)
    [----------] 1 test from DBCommon (453 ms total)
    ```