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
        # query = cursor.mogrify(base_query, var_tuple)
        cursor.execute(base_query, var_tuple)

        # if b'SELECT' in query or b'RETURNING' in query:
        #
        result = cursor.fetchall()
        # else:
        #     result = None
        database.commit()

        return result

def save_user_info(tarot_id, emotion_id, intention_cd):
    user_query = "UPDATE IT_USER_MAS A, " \
                    "(SELECT 'TEST0001' AS USER_ID, "  \
                        "F.TAROT_ID, T.TAROT_NM, F.EMOTION_ID, E.EMOTION_NM, F.FORTUNE_ID, F.INTENTION_CD, F.INTENTION_NM " \
		            "FROM IT_FORTUNE_MAS F, IT_EMOTION_MAS E, IT_TAROT_MAS T " \
		            "WHERE F.tarot_id = %s "\
                        "AND F.emotion_id = ( CASE %s "\
				            "WHEN '0'  THEN 'EM00' " \
				            "WHEN '1'  THEN 'EM01' " \
								    "END) " \
		                "AND intention_cd = %s " \
		                "AND F.tarot_id = T.tarot_id " \
		                "AND F.emotion_id = E.emotion_id) B " \
                    "SET A.TAROT_ID = B.TAROT_ID, " \
	                "A.TAROT_NM = B.TAROT_NM, " \
                    "A.EMOTION_ID = B.EMOTION_ID, " \
                    "A.EMOTION_NM = B.EMOTION_NM, " \
                    "A.INTENTION_NM = B.INTENTION_NM, " \
                    "A.FORTUNE_ID = B.FORTUNE_ID " \
	                    "WHERE A.USER_ID = B.USER_ID"
    secure_query(user_query, (tarot_id, emotion_id, intention_cd))

def get_data():
    data_query = "SELECT " \
                 "F.INTENTION_NM,F.INTENTION_CD,F.FORTUNE_DESC,U.TAROT_NM, " \
                 "U.TAROT_ID, U.EMOTION_NM, U.EMOTION_ID, " \
                    "( CASE U.EMOTION_ID " \
		                "WHEN 'EM00'  THEN '0' " \
		                "WHEN 'EM01'  THEN '1' " \
	                "END) AS EMOTION_ID, T.IMAGE_PATH " \
                "FROM IT_FORTUNE_MAS F, " \
                "IT_USER_MAS U, IT_TAROT_MAS T " \
                "WHERE USER_ID = 'TEST0001' "\
                "AND F.FORTUNE_ID = U.FORTUNE_ID "\
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






