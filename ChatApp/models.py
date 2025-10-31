# グループクラス
class Group:
    # b-8で使用
    @classmethod
    def create(cls, uid, new_group_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO `groups` (name, created_by) VALUES (%s, %s);"
                cur.execute(sql, (new_group_name, uid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'データベースの登録でエラーが発生しました：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    # b-8で使用
    @classmethod
    def find_by_name(cls, group_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = 'SELECT * FROM `groups` WHERE name = %s;'
                cur.execute(sql, (group_name,))
                group = cur.fetchone()
                return group
        except pymysql.Error as e:
            print(f'データベースの検索でエラーが発生しました：{e}')
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