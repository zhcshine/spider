# -*- encoding: utf8 -*-
import ConnectDatabase.MysqlConnect as MysqlConnect


class DbManager:
    def __init__(self, db_config):
        self.connect_config = db_config.connect_config()

    def mysql_connect(self):
        mysql_config = self.connect_config['mysql']
        self.mysql_connect = MysqlConnect.MysqlConnect(mysql_config)
        return self.mysql_connect

    def sql_server_connect(self):
        sql_server_config = self.connect_config['sql_server']
        self.sql_server_connect = MysqlConnect.MysqlConnect(sql_server_config)
        return self.sql_server_connect

def main():
        print u"请传入数据库配置信息"

if __name__ == '__main__':
    main()