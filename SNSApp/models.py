from flask import abort
import pymysql
from util.DB import DB

db_pool = DB.init_db_pool()

class User:

    # << 列名はドスターさんに要確認 >>
    # Email, パスワードは個人情報のアカウント設定も一緒のページ

    target_info = ['user_name', 'email', 'password', 'profile', 'updated_at', 'created_at']

    @classmethod
    def create(cls, user_name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (user_name, email, password) VALUES (%s, %s, %s);"

                # << タイムスタンプはSQL側で登録するのでこちらでは登録の必要はない？ >> 

                cur.execute(sql, (user_name, email, password))
                conn.commit()
                return cur.lastrowid
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_user_info(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
                info = []
                for t in cls.target_info:
                    info.append(user[t])

            return info if user else None
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def register_user_info(cls, user_id, **kwargs):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                for token in kwargs.keys():
                    if not token in cls.target_info:
                        raise ValueError('トークン名が一致していません')
                    
                    if kwargs[token] and token != 'created_at':
                        sql = f"INSERT INTO users ({token}) VALUES ({kwargs[token]});"
                        cur.execute(sql)
                        conn.commit()

        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE email=%s;"
                cur.execute(sql, (email,))
                user = cur.fetchone()
            return user
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)