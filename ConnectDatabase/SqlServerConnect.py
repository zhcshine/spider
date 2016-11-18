# -*- encoding: utf8 -*-
import pyodbc


class SqlServerConnect:
    """ Python连接SqlServer数据库类, 包含初始化变量，CURD操作，分页操作(等待补充)"""

    def __init__(self, connect_config):
        self.drive = connect_config['drive'] if 'drive' in connect_config.keys() else '{SQL Server}'
        self.port = connect_config['port'] if 'port' in connect_config.keys() else 1134
        self.server = connect_config['server'] if 'server' in connect_config.keys() else '127.0.0.1'
        self.database = connect_config['database']
        self.username = connect_config['username'] if 'username' in connect_config.keys() else 'sa'
        self.password = connect_config['password'] if 'password' in connect_config.keys() else ''
        if not self.database:
            raise(NameError, "please set the database name.")
        self.conn = pyodbc.connect(
                DRIVER=self.drive,
                PORT=self.port,
                SERVER=self.server,
                DATABASE=self.database,
                UID=self.username,
                PWD=self.password,
                charset='UTF-8'
        )
        self.cur = self.conn.cursor()
        if not self.cur:
            raise(NameError, "connected failed, please check the connected information")

    def exec_query(self, sql):
        self.cur.execute(sql)  # 通过指针来执行sql指令
        ret = self.cur.fetchall()  # 通过指针来获取sql指令响应数据
        return ret

    def exec_no_query(self, sql):
        self.cur.execute(sql)
        self.conn.commit()  # 连接句柄来提交

    def close(self):
        self.cur.close()
        self.conn.close()

    def __del__(self):
        self.close()


def main():
    print '请初始化配置信息OdbcSqlServer(drive, server, database, username, password)'


if __name__ == '__main__':
    main()
