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
               # SQLを実行し、パラメータ（uid, name, email, password）を埋め込む
               cur.execute(sql, (uid, name, email, password,))
               # データベースに変更を反映（保存）する
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)