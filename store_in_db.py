import MySQLdb
import time


HOST = '127.0.0.1'
DB_NAME = 'XXX'
DB_USER = 'root'
DB_PWD = '123456'
TB_NAME = "t_params"
PORT = 3306


class SessionStorage(object):

    def get(self, key, default=None):
        raise NotImplementedError()

    def set(self, key, value, ttl=None):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def __getitem__(self, key):
        self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)


class TokenStorage(SessionStorage):
    def __init__(self):
        pass

    def get(self, key, default=None):
        token = ""
        conn_a = MySQLdb.connect(db=DB_NAME, user=DB_USER, passwd=DB_PWD, host=HOST, port=PORT)
        cur_a = conn_a.cursor()

        # 判断时间
        sql_str = "SELECT * FROM %s WHERE k='%s';" % (TB_NAME, key+"_expire")
        cur_a.execute(sql_str)
        rows = cur_a.fetchall()
        if not rows:
            pass
        else:
            expire = rows[0][1]
            now = time.time()
            if now > float(expire):
                XXX.fetch_access_token()
                self.set(key+"_expire", str(now+3600))

        # 获取token
        sql_str = "SELECT * FROM %s WHERE k='%s';" % (TB_NAME, key)
        cur_a.execute(sql_str)
        rows = cur_a.fetchall()
        if not rows:
            pass
        else:
            token = rows[0][1]

        cur_a.close()
        conn_a.close()
        return token

    def set(self, key, value, ttl=None):
        if value is None:
            return
        conn_a = MySQLdb.connect(db=DB_NAME, user=DB_USER, passwd=DB_PWD, host=HOST, port=PORT)
        cur_a = conn_a.cursor()
        sql_str = "SELECT * FROM %s WHERE k='%s';" % (TB_NAME, key)
        cur_a.execute(sql_str)
        rows = cur_a.fetchall()
        if not rows:
            sql_str = "INSERT INTO %s values('%s', '%s')" % (TB_NAME, key, "")
            cur_a.execute(sql_str)
            sql_str = "INSERT INTO %s values('%s', '%s')" % (TB_NAME, key+"_expire", "0")
            cur_a.execute(sql_str)
            conn_a.commit()
        sql_str = "UPDATE %s SET v='%s' WHERE k='%s';" % (TB_NAME, value, key)
        cur_a.execute(sql_str)
        conn_a.commit()
        cur_a.close()
        conn_a.close()

    def delete(self, key):
        self._data.pop(key, None)
