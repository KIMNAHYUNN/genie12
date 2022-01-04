#############################################################
#############################################################

### db_utils.py: 웹 서버와 DB 연결, 쿼리문 등

#############################################################
#############################################################

import pymysql
from flask import g

def connect_db():
    """MySQL과 연결"""
    try:
        # 파라미터 지정
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
    """
    Flask에서 기본적으로 제공해주는 전역 변수 g에
    connect_db() 의 return value인 connection 객체 저장
    """
    if 'db' not in g:
        g.db = connect_db()
    return g.db

def secure_query(base_query, var_tuple):
    """
    get_db()에 저장된 connection 객체로부터 cursor() 호출 - Cursor 객체를 가져오고,
    Cursor 객체의 execute() 사용하여 SQL 문장을 DB 서버에 전송
    """
    database = get_db()

    with database.cursor() as cursor:
        # query = cursor.mogrify(base_query, var_tuple)
        # base_query: 사용되는 SQL 문장
        # var_tuple: SQL 문장에 binding 되는 값
        cursor.execute(base_query, var_tuple)

        # if b'SELECT' in query or b'RETURNING' in query:
        #
        result = cursor.fetchall()
        # else:
        #     result = None
        database.commit()   # commit

        return result

#############################################################
#############################################################

# emotion_id 를 DB에 저장
def save_emotion_id(emotion_id):
    save_query = "UPDATE IT_USER_MAS SET EMOTION_ID = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [emotion_id])

# intention_nm 을 DB에 저장
def save_intention_nm(intention_nm):
    save_query = "UPDATE IT_USER_MAS SET INTENTION_NM = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [intention_nm])

# tarot_id 를 DB에 저장
def save_tarot_id(tarot_id):
    save_query = "UPDATE IT_USER_MAS SET TAROT_ID = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [tarot_id])

# tarot_result 를 DB에 저장
def save_tarot_result(tarot_result):
    save_query = "UPDATE IT_USER_MAS SET TAROT_RESULT = %s WHERE USER_ID = 'TEST0001'"
    secure_query(save_query, [tarot_result])

# fortune_id, tarot_nm, emotion_nm 을 DB에 저장
def save_user_info():
    user_query = "UPDATE IT_USER_MAS U, IT_FORTUNE_MAS F,IT_EMOTION_MAS E, IT_TAROT_MAS T " \
                "SET U.FORTUNE_ID = F.FORTUNE_ID, U.TAROT_NM = T.TAROT_NM, U.EMOTION_NM = E.EMOTION_NM " \
                "WHERE U.INTENTION_NM = F.INTENTION_NM " \
                    "AND U.TAROT_ID = F.TAROT_ID " \
                    "AND U.EMOTION_ID = F.EMOTION_ID " \
                    "AND U.TAROT_ID = T.TAROT_ID " \
                    "AND U.EMOTION_ID = E.EMOTION_ID"
    secure_query(user_query, ())

# tarot_id를 DB에서 가져옴 
def get_tarot_id():
    data_query = "SELECT TAROT_ID FROM IT_USER_MAS WHERE USER_ID = 'TEST0001'"
    tarot_id = secure_query(data_query, ())
    return tarot_id[0][0]

# DB에서 필요한 정보를 가져옴
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

# file end