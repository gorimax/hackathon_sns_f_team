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
    def find_by_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM users WHERE user_id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user
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

    @classmethod
    def get_name_by_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT user_name FROM users WHERE user_id=%s;"
                cur.execute(sql, (user_id,))
                user = cur.fetchone()
            return user['user_name'] if user else None
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update_profile(cls, user_id, profile, learning):
        conn =db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """UPDATE users SET profile = %s,learning = %s
                         WHERE user_id = %s"""
                cur.execute(sql,(profile, learning, user_id))
            conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています: {e}")
            conn.rollback()
        finally:
            db_pool.release(conn)
class Post:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT * FROM posts
                         WHERE deleted_at IS NULL
                         ORDER BY created_at DESC;"""
                cur.execute(sql)
                posts = cur.fetchall()
            return posts
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def create(cls, user_id, content):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO posts (user_id, content) VALUES (%s, %s);"
                cur.execute(sql, (user_id, content))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE posts SET deleted_at = NOW() WHERE post_id=%s;"
                cur.execute(sql, (post_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM posts WHERE post_id=%s AND deleted_at IS NULL;"
                cur.execute(sql, (post_id,))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def get_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT * FROM posts
                         WHERE user_id=%s AND deleted_at IS NULL
                         ORDER BY post_id DESC;"""
                cur.execute(sql, (user_id))
                post = cur.fetchall()
            return post
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_post_by_post_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT posts.*,users.user_name FROM posts JOIN users
                         ON posts.user_id=users.user_id 
                         WHERE post_id=%s AND posts.deleted_at IS NULL;"""
                cur.execute(sql, post_id)
                last_id = cur.fetchone()
                return last_id
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_last_post_id(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT MAX(post_id) FROM posts;"
                cur.execute(sql)
                last_post_id = cur.fetchone()
                return last_post_id
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class Comment:
    @classmethod
    def create(cls, user_id, post_id, content):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO comments (user_id, post_id, content) VALUES (%s, %s, %s);"
                cur.execute(sql, (user_id, post_id, content))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_by_post_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT * FROM comments
                         WHERE post_id=%s AND deleted_at IS NULL
                         ORDER BY created_at DESC;"""
                cur.execute(sql, (post_id,))
                comments = cur.fetchall()
            return comments
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, comment_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT * FROM comments
                         WHERE comment_id=%s AND deleted_at IS NULL;"""
                cur.execute(sql, (comment_id,))
                post = cur.fetchone()
            return post
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, comment_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE comments SET deleted_at = NOW() WHERE comment_id=%s;"
                cur.execute(sql, (comment_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class Tag:
    @classmethod
    def get_tags(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM tags;"
                cur.execute(sql)
                tags = cur.fetchall()
            return tags
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_tags_post_id(cls, post_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT * FROM tags JOIN post_tags
                         ON tags.tag_id=post_tags.tag_id
                         WHERE post_id=%s;"""
                cur.execute(sql, (post_id))
                tag = cur.fetchall()
                return tag
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)           
    @classmethod
    def get_tag(cls, tag_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * from tags WHERE tag_id=%s;"
                cur.execute(sql,(tag_id,))
                tag = cur.fetchone()
                return tag
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, tag_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT * FROM post_tags WHERE tag_id=%s
                         ORDER BY post_id DESC;"""
                cur.execute(sql,(tag_id,))
                tag_posts = cur.fetchall()
                return tag_posts
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def set_tag_for_post(cls, last_post_id, tag_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s);"
                cur.execute(sql, (last_post_id, tag_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class Follow:
    @classmethod
    def get_followers_of_user(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT f.followed_user_id, u.user_name
                         FROM follow AS f JOIN users AS u ON f.user_id=u.user_id
                         WHERE f.followed_user_id=%s;"""
                cur.execute(sql, (user_id))
                followers = cur.fetchall()
                return followers
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
        
    @classmethod
    def get_following_users(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """SELECT f.user_id, u.user_name
                         FROM follow AS f JOIN users AS u
                         ON f.followed_user_id=u.user_id
                         WHERE f.user_id=%s;"""
                cur.execute(sql, (user_id))
                follow = cur.fetchall()
                return follow
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

class Bookmark:
    @classmethod
    def get_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM bookmarks WHERE user_id=%s;"
                cur.execute(sql, (user_id))
                bookmark = cur.fetchall()
                return bookmark
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)          