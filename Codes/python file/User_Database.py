# The creation of the user database is the same as that of the History_Database and Local_Database.
# Annotations could be referred to History_Database

import sqlite3

DATEBASE_NAME = 'user.db'

def sqlite_creat_table():
    conn = sqlite3.connect(DATEBASE_NAME)
    print("Opened database successfully")
    cursor = conn.cursor()

    try:
        sql = 'CREATE TABLE user(username  varchar(50), password varchar(50))'
        cursor.execute(sql)
    except:
        print("table is already available")

    cursor.close()
    conn.commit()
    conn.close()

def sqlite_insert(UserName_Sign_p,password_p):
    conn = sqlite3.connect(DATEBASE_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user VALUES('%s','%s')"%(UserName_Sign_p,password_p))

    cursor.close()
    conn.commit()
    conn.close()

def sqlite_find(UserName_Sign_p):
    conn = sqlite3.connect(DATEBASE_NAME)
    cursor = conn.cursor()

    cursor.execute("select * from user where username='%s'"%(UserName_Sign_p))
    value = cursor.fetchone()

    cursor.close()
    conn.commit()
    conn.close()

    return value

def sqlite_login(UserName_Sign_p,password_p):
    conn = sqlite3.connect(DATEBASE_NAME)
    cursor = conn.cursor()

    cursor.execute("select * from user where username='%s' AND password='%s'"%(UserName_Sign_p,password_p))
    value = cursor.fetchone()

    cursor.close()
    conn.commit()
    conn.close()

    return value

def sqlite_list():
    conn = sqlite3.connect(DATEBASE_NAME)
    cursor = conn.cursor()

    cursor.execute("select * from user")
    value = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    return value