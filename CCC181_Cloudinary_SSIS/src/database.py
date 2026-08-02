import pymysql
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST

def db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )