class Message:
    # b-14で使用
    @classmethod
    def create(cls, uid, gid, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages (uid, gid, message) VALUES (%s, %s, %s);" 
                # TIMESTANPはDBのカラム定義に「DEFAULT CURRENT_TIMESTAMP」を指定することによって自動的に入る
                cur.execute(sql,(uid, gid, message,))
                conn.commit()
        except pymysql.Error as e:
            print(f'データベースの登録でエラーが発生しました：{e}')
            abort(500)
        finally:
            db_pool.release(conn)