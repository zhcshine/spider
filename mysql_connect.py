# -*- encoding: utf8 -*-
import db_config
import ConnectDatabase.MysqlConnect as MysqlConnect

""" 配置mysql连接 """
connect_config = db_config.connect_config()
mysql_config = connect_config['mysql']
mysql_connect = MysqlConnect.MysqlConnect(mysql_config)


def db_connect():
    return mysql_connect
