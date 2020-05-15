# 记录
1. OpenSSL库的版本
只有某些版本的构建脚本能够成功.目前只能使用openssl/1.0.2t.如果设置openssl/1.1.1g,windows平台错误如下:
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
2. arm上加SQLITE_USER_AUTHENTICATION的宏定义也会提示找不到文件.