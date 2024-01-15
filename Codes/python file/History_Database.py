import sqlite3

DATEBASE_NAME = 'history.db'

def sqlite_creat_table():
    conn = sqlite3.connect(DATEBASE_NAME)
    print("Opened database successfully")
    # Create a cursor
    cursor = conn.cursor()

    # Create a table
    try:
        sql = 'CREATE TABLE user(username  varchar(100), time varchar(100), photo_url varchar(100), tag varchar(100), spider_result_name varchar(100), spider_result_url varchar(100))'
        cursor.execute(sql)
    except:
        print("table is already available")

    # Close the cursor
    cursor.close()
    conn.commit()
    # Close the connection
    conn.close()

def sqlite_insert(UserName_Sign_p, Time_p, Photo_Url_p, Tag_p,Spider_Result_name_p, Spider_Result_url_p):
    conn = sqlite3.connect(DATEBASE_NAME)
    cursor = conn.cursor()
    temp = Spider_Result_name_p.replace("\'"," ") # Change ' into a spacing to enhance the accuracy of the stored data and avoid errors
    Spider_Result_name_p = temp

    temp = Tag_p.replace("\'", " ")
    Tag_p = temp

    cursor.execute("INSERT INTO user VALUES('%s','%s', '%s', '%s', '%s', '%s')"%(UserName_Sign_p, Time_p, Photo_Url_p, Tag_p, Spider_Result_name_p, Spider_Result_url_p))

    cursor.close()
    conn.commit()
    conn.close()

def sqlite_list():
    conn = sqlite3.connect(DATEBASE_NAME)
    cursor = conn.cursor()

    cursor.execute("select * from user") # * Indicates the default choice is considering all keys
    value = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    return value