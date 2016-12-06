# -*- encoding: utf8 -*-
import sys
from spider_config import spider_config
from Initialization import Initialization
from UrlCraw import UrlCraw
from UrlAnalyse import UrlAnalyse
import db_config
import ConnectDatabase.MysqlConnect as MysqlConnect
import multiprocessing
import os
reload(sys)
sys.setdefaultencoding("utf-8")

# 根据id自增的url地址
# 将需要递增的id改成****
# python id_spider.py http://www.xxx.com?id=**** 0 4000000 1


""" 初始化爬虫 """
# 获取简易版url，去除参数，去除http，https
url_argv_base = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
step = sys.argv[4]
# 将传入的url地址id改成1
url_argv = url_argv_base.replace('****', '1')
initialization = Initialization.Initialization(url_argv)
base_url = initialization.initialization_url()
table = initialization.initialization_create_table(base_url)
initialization.initialization_close()

# 是否设置代理
spider_config = spider_config()
proxy = spider_config['proxy']


def spider(i):
    """ 配置mysql连接 """
    connect_config = db_config.connect_config()
    mysql_config = connect_config['mysql']
    mysql_connect = MysqlConnect.MysqlConnect(mysql_config)
    url_craw = UrlCraw.UrlCraw()
    url_analyse = UrlAnalyse.UrlAnalyse()
    sql_data = {
        'pid': i,
        'url': url_argv_base.replace('****', str(i)),
    }
    sql = 'SELECT id, pid, url, is_crawed, retry FROM `{}` WHERE url LIKE \'{}\''.format(table, sql_data['url'])
    result = mysql_connect.query(sql)
    if result:
        record = mysql_connect.fetch_one()
        url_recode = {
            'id': record[0],
            'pid': record[1],
            'url': record[2],
            'is_crawed': record[3],
            'retry': record[4]
        }
        if not url_recode['is_crawed']:
            response = url_craw.craw(url_recode=url_recode)
            url_analyse.id_spider_analyse(table=table, response=response)
        else:
            mysql_connect.commit()
    else:
        sql_data = {
            'pid': i,
            'url': url_argv_base.replace('****', str(i)),
            'is_crawed': 0,
            'retry': 3,
        }
        mysql_connect.insert(table, sql_data)
        mysql_connect.commit()
        sql = 'SELECT id, pid, url, is_crawed, retry FROM `{}` WHERE url LIKE \'{}\''.format(table, sql_data['url'])
        result = mysql_connect.query(sql)
        if result:
            record = mysql_connect.fetch_one()
            url_recode = {
                'id': record[0],
                'pid': record[1],
                'url': record[2],
                'is_crawed': record[3],
                'retry': record[4]
            }
            response = url_craw.craw(url_recode=url_recode)
            url_analyse.id_spider_analyse(table=table, response=response)
        else:
            mysql_connect.commit()

current_pid = os.getpid()
print u'当前进程号：' , str(current_pid)
p = multiprocessing.Pool()
for i in range(int(start), int(end), int(step)):
    p.apply_async(spider, args={i, })
p.close()
p.join()