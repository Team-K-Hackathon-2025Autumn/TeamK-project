from flask import abort
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# ユーザークラス
class User:
    @classmethod
    def create(cls, uid, name, email, password):
        # データベース接続プールからコネクションを取得する
        conn = db_pool.get_conn()
        try:
            # コネクションからカーソル（操作用のオブジェクト）を取得する
            with conn.cursor() as cur:
                sql = "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s);"
                # SQLを実行し、パラメータ（id, name, email, password）を埋め込む
                cur.execute(
                    sql,
                    (
                        uid,
                        name,
                        email,
                        password,
                    ),
                )
                # データベースに変更を反映（保存）する
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
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
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)



# グループクラス
class Group:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM `groups`;"
                cur.execute(sql)
                groups = cur.fetchall()
                return groups
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
        finally:
            db_pool.release(conn)
   
    # b-8で使用
    @classmethod
    def create(cls, uid, new_group_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO `groups` (name, created_by) VALUES (%s, %s);"
                cur.execute(sql, (new_group_name, uid,))
                conn.commit()
                return cur.lastrowid
        except pymysql.Error as e:
            print(f'データベースの登録でエラーが発生しました：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
class Member:
    # b-8で使用
    @classmethod
    def add(cls, uid ,gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'INSERT INTO user_groups VALUES (%s, %s);'
                cur.execute(sql,(uid, gid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'データベースの登録でエラーが発生しました（user_groups)：{e}')
            abort(500)
        finally:
            db_pool.release(conn)