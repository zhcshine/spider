# -*- encoding: utf8 -*-
from urlparse import urlparse
import MySQLdb
import db_config
import ConnectDatabase.MysqlConnect as MysqlConnect

class Initialization:
    def __init__(self, url):
        self.url = url.lower()
        """ 配置mysql连接 """
        connect_config = db_config.connect_config()
        mysql_config = connect_config['mysql']
        self.mysql_connect = MysqlConnect.MysqlConnect(mysql_config)


    def initialization_url(self):
        url_parse = urlparse(self.url)
        if url_parse.scheme:
            base_url = url_parse.scheme + '://' + url_parse.netloc
        else:
            base_url = 'http://' + url_parse.netloc
        print u'您需要爬取的url链接为：' + base_url
        return base_url

    def initialization_create_table(self, base_url):
        # 数据表名称
        url_parse = urlparse(self.url)
        table = url_parse.netloc.replace('.', '_').replace('-', '_') + '_urls'
        sql = 'CREATE TABLE `{}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `pid` INT(11) NOT NULL , `url` VARCHAR(300) NOT NULL , `is_crawed` INT(1) NOT NULL , `retry` INT(1) NOT NULL , `code` VARCHAR(100) NULL DEFAULT NULL , `html` LONGTEXT NULL DEFAULT NULL , PRIMARY KEY (`id`), INDEX (`pid`), INDEX (`url`), INDEX (`is_crawed`)) ENGINE = InnoDB;'.format(table)
        try:
            self.mysql_connect.cur.execute(sql)
        except MySQLdb.Error as e:
            print e

        sql = 'SELECT id, url, is_crawed FROM {}'.format(table)
        results = self.mysql_connect.query(sql)
        if results == 0:
            sql_data = {
                'pid': 0,
                'url': self.url,
                'is_crawed': 0,
                'retry': 3
            }
            self.mysql_connect.insert(table, sql_data)
            self.mysql_connect.commit()
        return table

    def initialization_close(self):
        self.mysql_connect.close()