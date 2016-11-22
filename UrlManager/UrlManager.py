# -*- encoding: utf8 -*-
import sys
from mysql_connect import db_connect
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")


class UrlManager:
    def __init__(self):
        pass

    def has_craw_url(self, table):
        sql = 'SELECT id, pid, url, is_crawed, retry, code FROM {} WHERE is_crawed LIKE 0'.format(table)
        results = db_connect().query(sql)
        if results == 0:
            print u'没有需要爬取的url了，即将退出程序'
            return 0
        else:
            return 1

    def get_one_url(self, table):
        sql = 'SELECT id, pid, url, is_crawed, retry, code FROM {} WHERE is_crawed LIKE 0'.format(table)
        results = db_connect().query(sql)
        if results == 0:
            print u'没有需要爬取的url了，即将退出程序'
            return 0
        else:
            print u'剩余爬取数量: ' + str(results)
            record = db_connect().fetch_one()
            result = {
                'id': record[0],
                'pid': record[1],
                'url': record[2],
                'is_crawed': record[3],
                'retry': record[4]
            }
            return result

def main():
    print u"请传入表名称"

if __name__ == '__main__':
    main()