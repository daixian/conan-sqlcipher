#include <sqlcipher/sqlite3.h>

int sqlite_callback(
    void* pv,    /* 由 sqlite3_exec() 的第四个参数传递而来 */
    int argc,    /* 表的列数 */
    char** argv, /* 指向查询结果的指针数组, 可以由 sqlite3_column_text() 得到 */
    char** col   /* 指向表头名的指针数组, 可以由 sqlite3_column_name() 得到 */
)
{
}

int main()
{
    remove("test.db3");
    char* zErrMsg = NULL;
    sqlite3* db;
    // sqlite3_open(":memory:", &db);
    sqlite3_open("test.db3", &db);
    int ret = sqlite3_key(db, "toto", 5);
    //这个函数调用之前好像必须要先调用key
    ret = sqlite3_rekey(db, "toto123", 7);

    sqlite3_exec(db,
        "CREATE TABLE sys_info (id INTEGER PRIMARY KEY, dev_id INTEGER, dev_id_byte BLOB, dev_id_base64 TEXT, dev_ver TEXT, soft_ver TEXT, calib_ver TEXT)",
        sqlite_callback, NULL, zErrMsg);

    sqlite3_close(db);
    return ret;
}
