import sqlite3
from datetime import datetime

str_db = "web_db"
str_table = "user_data"


def use_my_database(): # 共用程式碼 資料庫連結 & 取得 conn, cursor
    global str_db
    conn = sqlite3.connect(str_db)
    cursor = conn.cursor()
    return conn, cursor


def create_table(): # 建立資料表
    global str_table
    conn, cursor = use_my_database()
    cursor.execute(f"create table {str_table} (uid int primary key, name content varchar(20), content varchar(20))")


def insert_data(name, str_contest): # 新增資料
    conn, cursor = use_my_database()
    unix_num = int(datetime.now().timestamp())
    cursor.execute("INSERT INTO user_data(UID, NAME,CONTENT) VALUES (?, ?, ?)", (unix_num, name, str_contest))
    conn.commit()


def query_datas(): # 取得所有資料
    global str_table
    conn, cursor = use_my_database()
    cursor.execute(f"select * from {str_table}")
    conn.row_factory = sqlite3.Row
    datas = cursor.fetchall()

    list_datas = []
    str_column = []
    for i in cursor.description:
        str_column.append(i[0])

    for uint in datas:
        temp = {}
        for i in range(len(str_column)):
            temp[str_column[i]] = uint[i]

        list_datas.append(temp)

    return list_datas


def find_data(uid): # 查詢資料
    global str_table
    conn, cursor = use_my_database()
    cursor.execute(f"select * from {str_table} where UID={uid}")
    data = cursor.fetchone()
    return data


def update_data(uid, name, content): # 修改資料
    global str_table
    conn, cursor = use_my_database()
    cursor.execute("update user_data set NAME=?, CONTENT=? where UID=?", (name, content, uid))
    conn.commit()


def delete_data(uid): # 刪除資料
    global str_table
    conn, cursor = use_my_database()
    cursor.execute(f"delete from {str_table} where UID={uid}")
    conn.commit()


# # 1. 建立資料表
# create_table()
#
# # 2. 新增測試資料
# insert_data("Bob", "BMW-8787")
#
# #3. 查詢資料庫
# datas = query_datas()
# if None != query_datas():
#     print(datas)
#     print(datas[0][0])
#     data = find_data(datas[0][0])
#     print(data)
#
# # 4. 修改資料
# datas = query_datas()
# if None != query_datas():
#     data = find_data(datas[0][0])
#     update_data(datas[0][0], "Sam", "SUV-6969")
#     data = find_data(datas[0][0])
#     print(data)
#
# # 5. 刪除資料
# datas = query_datas()
# if None != query_datas():
#     print("before delete============")
#     print(query_datas())
#     data = find_data(datas[0][0])
#     delete_data(datas[0][0])
#     print("after delete============")
#     print(query_datas())