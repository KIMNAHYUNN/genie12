import pymysql
from flask import g
from PIL import Image
from io import BytesIO

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

def save_user_info(tarot_id, emotion_id):
    user_query = "UPDATE IT_USER_MAS SET TAROT_ID=%s, EMOTION_ID=%s WHERE USER_ID='TEST0001'"
    secure_query(user_query, (tarot_id, emotion_id))

def save_fortune_id(fortune_id):
    user_query = "UPDATE IT_USER_MAS SET fortune_id=%s WHERE USER_ID='TEST0001'"
    secure_query(user_query, [fortune_id])

def get_fortune_info(tarot_id, emotion_id):
    fortune_desc_query = "SELECT FORTUNE_DESC, FORTUNE_ID FROM IT_FORTUNE_MAS WHERE TAROT_ID=%s AND EMOTION_ID=%s"
    fortune = secure_query(fortune_desc_query, (tarot_id, emotion_id))[0][0]
    fortune_info = {
        'fortune_desc': fortune[0][0],
        'fortune_id': fortune[0][1]
    }
    return fortune_info

def get_tarot_info(tarot_id):
    tarot_info_query = "SELECT tarot_nm, image_data FROM IT_TAROT_MAS WHERE TAROT_ID=%s"
    tarot_info = secure_query(tarot_info_query, [tarot_id])
    tarot_nm = tarot_info[0][0]
    image_data = tarot_info[0][1]

    get_image = Image.open(BytesIO(image_data['image_data']))
    get_image = get_image.decode("UTF-8")

    tarot_info = {
        'tarot_nm':tarot_nm,
        'image_data':get_image
    }
    return tarot_info





