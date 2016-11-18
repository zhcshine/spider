# -*- encoding: utf8 -*-
# 生产环境将文件名改成db_config.py
sql_server_config = {
    'server': 'serverName',
    'username': 'sa',
    'password': 'password',
    'database': 'database'
}

mysql_config = {
    'server': 'localhost',
    'username': 'root',
    'password': 'password',
    'database': 'database',
}


def connect_config():
    return {
        'sql_server': sql_server_config,
        'mysql': mysql_config
    }