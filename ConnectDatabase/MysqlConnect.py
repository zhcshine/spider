# -*- encoding: utf8 -*-
# 下载安装
# window环境下： https://pypi.python.org/pypi/MySQL-python/1.2.5 下载.exe一键安装
# ubuntu安装步骤：
# sudo apt-get install python-setuptools
# sudo apt-get install libmysqld-dev
# sudo apt-get install libmysqlclient-dev
# sudo apt-get install python-dev
# sudo easy_install mysql-python

import MySQLdb
OperationalError = MySQLdb.OperationalError


class MysqlConnect:
    """ Python连接Mysql数据库类, 包含初始化变量，CURD操作，分页操作(等待补充)"""

    def __init__(self, connect_config):
        self.port = connect_config['port'] if 'port' in connect_config.keys() else 3306
        self.server = connect_config['server'] if 'server' in connect_config.keys() else '127.0.0.1'
        self.database = connect_config['database']
        self.username = connect_config['username'] if 'username' in connect_config.keys() else 'root'
        self.password = connect_config['password'] if 'password' in connect_config.keys() else ''
        self.charset = connect_config['charset'] if 'charset' in connect_config.keys() else 'utf8'
        try:
            self.conn = MySQLdb.connect(
                host=self.server,
                port=self.port,
                user=self.username,
                passwd=self.password,
                db=self.database
            )
            self.conn.autocommit(False)
            self.conn.set_character_set(self.charset)
            self.cur = self.conn.cursor()
        except MySQLdb.Error as e:
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    def close(self):
        """ 关闭数据库连接 """
        self.cur.close()
        self.conn.close()

    def select_db(self, db):
        """ 重新选择数据库 """
        try:
            self.conn.select_db(db)
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def query(self, sql):
        """ 查询语句直接返回的是查询到的数量(count) """
        try:
            n = self.cur.execute(sql)
            return n
        except MySQLdb.Error as e:
            print 'Mysql Error:%s\nSQL:%s' % (e, sql)

    def fetch_one(self):
        result = self.cur.fetchone()
        return result

    def fetch_all(self):
        result = self.cur.fetchall()
        desc = self.cur.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                _d[desc[i][0]] = str(inv[i])
                d.append(_d)
        return d

    def insert(self, table_name, data):
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        return self.cur.execute(_sql, tuple(_params))

    def update(self, table_name, data, condition):
        _fields = " "
        _prefix = "".join(['UPDATE `', table_name, '`', ' SET'])
        for key in data.keys():
            _fields += "%s = '%s', " % (key, data[key])
        _fields = _fields[:-2]
        _sql = "".join([_prefix, _fields, " WHERE ", condition])
        return self.cur.execute(_sql)

    def delete(self, table_name, condition):
        _prefix = "".join(['DELETE FROM  `', table_name, '`', 'WHERE'])
        _sql = "".join([_prefix, condition])
        return self.cur.execute(_sql)

    def get_last_insert_id(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __del__(self):
        self.close()


def main():
    print "请初始化配置信息{'server': 'localhost', 'database': 'database', 'username': 'root', 'password': 'password'}"

if __name__ == '__main__':
    main()
