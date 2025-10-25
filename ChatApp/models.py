from flask import abort
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


class Member:
    @classmethod
    def get_all(cls, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT ug.id, u.name, u.email
                    FROM user_groups AS ug INNER JOIN users AS u ON ug.uid = u.id
                    WHERE ug.gid = %s
                    ORDER BY ug.id ASC;
                """
                cur.execute(sql, (gid,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


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
