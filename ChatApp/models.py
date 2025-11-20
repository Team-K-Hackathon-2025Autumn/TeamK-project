from click import group
from flask import abort
import pymysql
from util.DB import DB

# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# ユーザークラス
class User:
    @classmethod
    def create(cls, uid, name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (id, name, email, password) VALUES (%s, %s, %s, %s);"
                cur.execute(
                    sql,
                    (
                        uid,
                        name,
                        email,
                        password,
                    ),
                )
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
    def find_by_uid(cls, uid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM `groups` WHERE id IN (SELECT gid FROM user_groups WHERE uid = %s)"
                cur.execute(sql, (uid,))
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
                sql = "SELECT * FROM `groups` WHERE id=%s;"
                cur.execute(sql, (gid,))
                group = cur.fetchone()
                return group
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def create(cls, uid, group_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO `groups` (name, created_by) VALUES (%s, %s);"
                cur.execute(
                    sql,
                    (
                        group_name,
                        uid,
                    ),
                )
                conn.commit()
                return cur.lastrowid
        except pymysql.Error as e:
            print(f"データベースの登録でエラーが発生しました：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, gid, new_group_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE `groups` SET name=%s WHERE id=%s;"
                cur.execute(sql, (new_group_name, gid))
                conn.commit()
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
                sql = "DELETE FROM `groups` WHERE id=%s;"
                cur.execute(sql, (gid,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


## メッセージクラス
class Message:
    @classmethod
    def get_all(cls, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT m.id, m.uid, u.name, m.creation_type, m.message, r.counts, m.created_at 
                    FROM messages AS m 
                    INNER JOIN users AS u ON m.uid = u.id
                    LEFT OUTER JOIN eat_reactions AS r ON m.id = r.message_id
                    WHERE m.gid = %s 
                    
                    UNION ALL
                    
                    SELECT am.id, '0' AS uid, 'AIからのメニュー提案' AS name, am.creation_type, am.message, ar.counts, am.created_at
                    FROM ai_messages AS am
                    LEFT OUTER JOIN ai_eat_reactions AS ar ON am.id = ar.message_id
                    WHERE am.gid = %s

                    ORDER BY created_at ASC;
                """
                cur.execute(sql, (gid, gid))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_mid(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT id, uid
                    FROM messages
                    WHERE id = %s;
                """
                cur.execute(sql, (message_id))
                message = cur.fetchone()
                return message
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def create(cls, uid, gid, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO messages (uid, gid, message) VALUES (%s, %s, %s);
                """
                # TIMESTANPはDBのカラム定義に「DEFAULT CURRENT_TIMESTAMP」を指定することによって自動的に入る
                cur.execute(
                    sql,
                    (
                        uid,
                        gid,
                        message,
                    ),
                )
                conn.commit()

            message_id = cur.lastrowid
            with conn.cursor() as cur:
                sql = """
                INSERT INTO eat_reactions (message_id, counts) VALUES (%s, 0);
                """
                # メッセージ作成時にeat_reactionsテーブルにリアクション数を0として挿入する
                cur.execute(
                    sql,
                    (message_id),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"データベースの登録でエラーが発生しました：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """DELETE FROM messages WHERE id = %s;
                """
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def ai_create(cls, gid, ai_message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO ai_messages(gid, message) VALUES(%s, %s)"
                cur.execute(
                    sql,
                    (
                        gid,
                        ai_message,
                    ),
                )
                conn.commit()

            message_id = cur.lastrowid
            with conn.cursor() as cur:
                sql = """
                INSERT INTO ai_eat_reactions (message_id, counts) VALUES (%s, 0);
                """
                # AIメッセージ作成時にai_eat_reactionsテーブルにリアクション数を0として挿入する
                cur.execute(
                    sql,
                    (message_id),
                )
                conn.commit()

        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


## メンバークラス
class Member:
    @classmethod
    def get_all(cls, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT id, name, email
                    FROM users WHERE id IN (SELECT uid FROM user_groups WHERE gid = %s)
                    ORDER BY name ASC;
                """
                cur.execute(sql, (gid,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def add(cls, uid, gid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO user_groups VALUES (%s, %s);"
                cur.execute(
                    sql,
                    (
                        uid,
                        gid,
                    ),
                )
                conn.commit()
        except pymysql.Error as e:
            print(f"データベースの登録でエラーが発生しました(user_groups)：{e}")
            abort(500)
        finally:
            db_pool.release(conn)


# リアクションクラス
class eatReaction:
    @classmethod
    def add(
        cls,
        message_id,
        message_creation_type,
    ):
        conn = db_pool.get_conn()
        try:
            if message_creation_type == "user":
                with conn.cursor() as cur:
                    sql = """
                        UPDATE eat_reactions SET counts = counts + 1
                        WHERE message_id = %s;
                    """
                    cur.execute(sql, (message_id,))
                    conn.commit()
            elif message_creation_type == "ai":
                with conn.cursor() as cur:
                    sql = """
                        UPDATE ai_eat_reactions SET counts = counts + 1
                        WHERE message_id = %s;
                    """
                    cur.execute(sql, (message_id,))
                    conn.commit()
        except pymysql.Error as e:
            print(f"エラーが発生しています：{e}")
            abort(500)
        finally:
            db_pool.release(conn)
