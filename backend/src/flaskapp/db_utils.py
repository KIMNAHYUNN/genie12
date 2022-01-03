import pymysql
from flask import g

def connect_db():
    try:
        db = pymysql.connect(
            host='125.142.194.152',
            port=3306,
            user='tarotadm',
            passwd='tarotadm123!',
            db='tarot', charset='utf8', autocommit=True)
        return db
    except Exception as ex:
        print("Can't connect to database")
        raise IOError

def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db

def secure_query(base_query, var_tuple):
    database = get_db()

    with database.cursor() as cursor:
        cursor.execute(base_query, var_tuple)
        result = cursor.fetchall()
        database.commit()
        return result

def save_emotion_id(emotion_id):
    save_query = "UPDATE IT_USER_MAS SET EMOTION_ID = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [emotion_id])

def save_intention_nm(intention_nm):
    save_query = "UPDATE IT_USER_MAS SET INTENTION_NM = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [intention_nm])

def save_tarot_id(tarot_id):
    save_query = "UPDATE IT_USER_MAS SET TAROT_ID = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [tarot_id])

def save_tarot_result(tarot_result):
    save_query = "UPDATE IT_USER_MAS SET TAROT_RESULT = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [tarot_result])

def save_user_info():
    user_query = "UPDATE IT_USER_MAS U, IT_FORTUNE_MAS F,IT_EMOTION_MAS E, IT_TAROT_MAS T " \
                "SET U.FORTUNE_ID = F.FORTUNE_ID, U.TAROT_NM = T.TAROT_NM, U.EMOTION_NM = E.EMOTION_NM " \
                "WHERE U.INTENTION_NM = F.INTENTION_NM " \
                    "AND U.TAROT_ID = F.TAROT_ID " \
                    "AND U.EMOTION_ID = F.EMOTION_ID " \
                    "AND U.TAROT_ID = T.TAROT_ID " \
                    "AND U.EMOTION_ID = E.EMOTION_ID"
    secure_query(user_query, ())

def get_tarot_id():
    data_query = "SELECT TAROT_ID FROM IT_USER_MAS WHERE USER_ID = 'TEST0001'"
    tarot_id = secure_query(data_query, ())
    return tarot_id[0][0]

def get_data():
    data_query = "SELECT " \
                 "F.INTENTION_NM,F.INTENTION_CD,F.FORTUNE_DESC,U.TAROT_NM, " \
                 "U.TAROT_ID, U.EMOTION_NM, U.EMOTION_ID, T.IMAGE_PATH " \
                "FROM IT_FORTUNE_MAS F, " \
                "IT_USER_MAS U, IT_TAROT_MAS T " \
                "WHERE USER_ID = 'TEST0001' " \
                "AND F.FORTUNE_ID = U.FORTUNE_ID " \
                "AND U.TAROT_ID = T.TAROT_ID"
    data = secure_query(data_query, ())
    info = {
        'intention_nm': data[0][0],
        'intention_cd': data[0][1],
        'fortune_desc': data[0][2],
        'tarot_nm': data[0][3],
        'tarot_id': data[0][4],
        'emotion_nm': data[0][5],
        'emotion_id': data[0][6],
        'image_path': data[0][7]
    }
    return info






