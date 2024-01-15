# Functions are the same as those used in History_Database. Annotations could be referred to those in History_Database

import sqlite3

DATEBASE1_NAME = 'local.db'

def sqlite_creat_table():
    conn = sqlite3.connect(DATEBASE1_NAME)
    print("Opened database successfully")
    cursor = conn.cursor()

    try:
        sql = 'CREATE TABLE user(username  varchar(100), time varchar(100), photo_url varchar(100), tag varchar(100), spider_result_name varchar(100), spider_result_scores varchar(100), spider_result_character varchar(100), spider_result_date varchar(100), spider_result_description varchar(100))'
        cursor.execute(sql)
    except:
        print("table is already available")

    cursor.close()
    conn.commit()
    conn.close()

def sqlite_insert(UserName_Sign_p, Time_p, Photo_Url_p, Tag_p,Spider_Result_name_p, Spider_Result_scores_p, Spider_Result_character_p, Spider_Result_date_p, Spider_Result_description_p):
    conn = sqlite3.connect(DATEBASE1_NAME)
    cursor = conn.cursor()
    temp = Spider_Result_name_p.replace("\'"," ")
    Spider_Result_name_p = temp

    temp = Spider_Result_scores_p.replace("\'", " ")
    Spider_Result_scores_p = temp

    temp = Spider_Result_character_p.replace("\'", " ")
    Spider_Result_character_p = temp

    temp = Spider_Result_date_p.replace("\'", " ")
    Spider_Result_date_p = temp

    temp = Spider_Result_description_p.replace("\'", " ")
    Spider_Result_description_p = temp

    temp = Tag_p.replace("\'", " ")
    Tag_p = temp

    cursor.execute("INSERT INTO user VALUES('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(UserName_Sign_p, Time_p, Photo_Url_p, Tag_p, Spider_Result_name_p, Spider_Result_scores_p, Spider_Result_character_p, Spider_Result_date_p, Spider_Result_description_p))

    cursor.close()
    conn.commit()
    conn.close()

def sqlite_list():
    conn = sqlite3.connect(DATEBASE1_NAME)
    cursor = conn.cursor()

    cursor.execute("select * from user")
    value = cursor.fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    return value