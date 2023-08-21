import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
# cursor.execute("drop table student")
# cursor.execute("create table student (id varchar(20) primary key, name varchar(20))")
cursor.execute('insert into student (id, name) values("123", "Tom")')
cursor.execute('insert into student (id, name) values("456", "Qjg")')
conn.commit()
print(cursor.rowcount)

cursor.execute("select * from student")
values = cursor.fetchall()