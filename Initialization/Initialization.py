# -*- encoding: utf8 -*-
from urlparse import urlparse
import MySQLdb



class Initialization():
    def __init__(self, db, config, url):
        self.url = url.lower()
        self.db = db
        self.config = config

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
        url_parse = urlparse(base_url)
        table = url_parse.netloc.replace('.', '_').replace('-', '_') + '_urls'
        sql = 'CREATE TABLE `{}` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `pid` INT(11) NOT NULL , `url` VARCHAR(300) NOT NULL , `is_crawed` INT(1) NOT NULL , `retry` INT(1) NOT NULL , `code` VARCHAR(100) NULL DEFAULT NULL , `html` LONGTEXT NULL DEFAULT NULL , PRIMARY KEY (`id`), INDEX (`pid`), INDEX (`url`), INDEX (`is_crawed`)) ENGINE = InnoDB;'.format(table)
        try:
            self.db.cur.execute(sql)
        except MySQLdb.Error as e:
            print e

        sql = 'SELECT id, url, is_crawed FROM {}'.format(table)
        results = self.db.query(sql)
        if results == 0:
            sql_data = {
                'pid': 0,
                'url': self.url,
                'is_crawed': 0,
                'retry': 3
            }
            self.db.insert(table, sql_data)
            self.db.commit()
        return table
