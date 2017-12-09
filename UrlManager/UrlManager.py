# -*- encoding: utf8 -*-
import sys
from SpiderPrint import SpiderPrint
reload(sys)
sys.setdefaultencoding("utf-8")


class UrlManager:
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.sprint = SpiderPrint.SpiderPrint()

    def get_one_url(self, table):
        sql = 'SELECT id, pid, url, is_crawed, retry, code FROM {} WHERE is_crawed = 0'.format(table)
        results = self.db.query(sql)
        if results == 0:
            print u'没有需要爬取的url了，即将退出程序'
            return 0
        else:
            record = self.db.fetch_one()
            self.sprint.print_msg(str(record[2]))
            self.sprint.print_spending_time('Current/Remain：', str(record[0]) + '/' + str(results))
            # 锁住此url，防止多进程运行时重复读取
            sql_data = {
                'is_crawed': 2,
            }
            condition = 'id = {}'.format(record[0])
            try:
                self.db.update(table, sql_data, condition)
                self.db.commit()
            except Exception, e:
                self.db.rollback()
                pass
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