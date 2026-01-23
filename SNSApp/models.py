
class User:

    # << 列名はドスターさんに要確認 >>
    # Email, パスワードは個人情報なので他のアカウント設定などで分けた方がいい？

    target_info = ['name', 'introduction', 'updated_timestamp', 'registered_timestamp']
    target_info_to_create = ['name', 'introduction', 'updated_timestamp']

    @classmethod
    def create(cls, name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s);"

                # << タイムスタンプはSQL側で登録するのでこちらでは登録の必要はない？ >> 

                cur.execute(sql, (name, email, password))
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
                    if not token in cls.target_info_to_create:
                        raise ValueError('トークン名が一致していません')
                    
                    if kwargs[token]:
                        sql = f"INSERT INTO users ({token}) VALUES ({kwargs[token]});"
                        cur.execute(sql)
                        conn.commit()

        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
