# -*- encoding: utf8 -*-
import sys
import db_config
import ConnectDatabase.MysqlConnect as MysqlConnect
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")


class UrlManager:
    def __init__(self):
        """ 配置mysql连接 """
        connect_config = db_config.connect_config()
        mysql_config = connect_config['mysql']
        self.mysql_connect = MysqlConnect.MysqlConnect(mysql_config)

    def has_craw_url(self, table):
        sql = 'SELECT id, pid, url, is_crawed, retry, code FROM {} WHERE is_crawed = 0'.format(table)
        results = self.mysql_connect.query(sql)
        if results == 0:
            print u'没有需要爬取的url了，即将退出程序'
            return 0
        else:
            return 1

    def get_one_url(self, table):
        sql = 'SELECT id, pid, url, is_crawed, retry, code FROM {} WHERE is_crawed = 0'.format(table)
        results = self.mysql_connect.query(sql)
        if results == 0:
            print u'没有需要爬取的url了，即将退出程序'
            return 0
        else:
            print u'剩余爬取数量: ' + str(results)
            record = self.mysql_connect.fetch_one()
            # 锁住此url，防止多进程运行时重复读取
            sql_data = {
                'is_crawed': 2,
            }
            condition = 'id = {}'.format(record[0])
            try:
                self.mysql_connect.update(table, sql_data, condition)
                self.mysql_connect.commit()
            except Exception, e:
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