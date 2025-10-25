from flask import abort
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# グループクラス
class Group:
    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM groups;"
                cur.execute(sql)
                groups = cur.fetchall()
                return groups
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_gid(cls, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM groups WHERE gid=%s;"
                cur.execute(sql, (gid,))
                groups = cur.fetchone()
                return groups
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, gid, new_group_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE groups SET name=%s, WHERE id=%s;"
                cur.execute(sql, (gid, new_group_name))
                conn.commit()
                groups = cur.fetchall()
                return groups
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE * FROM groups WHERE gid=%s;"
                cur.execute(sql, (gid,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


# メッセージクラス
class Message:
    @classmethod
    def get_all(cls, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT m.id, m.uid, u.name, m.message, r.counts, m.created_at 
                    FROM messages AS m 
                    INNER JOIN users AS u ON m.uid = u.id
                    INNER JOIN eat_reactions AS r ON m.id = r.message_id 
                    WHERE m.gid = %s 
                    ORDER BY m.id ASC;
                """
                cur.execute(sql, (gid,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)
