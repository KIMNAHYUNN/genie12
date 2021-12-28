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
        query = cursor.mogrify(base_query, var_tuple)
        cursor.execute(query)

        if b'SELECT' in query or b'RETURNING' in query:
            result = cursor.fetchall()
        else:
            result = None
        database.commit()

        return result
