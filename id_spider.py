# -*- encoding: utf8 -*-
import sys
from spider_config import spider_config
from Initialization import Initialization
from UrlManager import UrlManager
from UrlCraw import UrlCraw
from UrlAnalyse import UrlAnalyse
from mysql_connect import db_connect
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

# 根据id自增的url地址
# 将需要递增的id改成****
# python id_spider.py http://www.xxx.com?id=**** 4000000


""" 初始化爬虫 """
# 获取简易版url，去除参数，去除http，https
url_argv_base = sys.argv[1]
end_num = sys.argv[2]
# 将传入的url地址id改成1
url_argv = url_argv_base.replace('****', '1')
initialization = Initialization.Initialization(url_argv)
base_url = initialization.initialization_url()
table = initialization.initialization_create_table(base_url)
# 是否设置代理
spider_config = spider_config()
proxy = spider_config['proxy']

has_craw_url = UrlManager.UrlManager()
url_manager = UrlManager.UrlManager()
url_craw = UrlCraw.UrlCraw()
url_analyse = UrlAnalyse.UrlAnalyse()



for i in range(int(end_num)):
    sql_data = {
        'pid': i,
        'url': url_argv_base.replace('****', str(i)),
    }
    sql = 'SELECT id, pid, url, is_crawed, retry FROM `{}` WHERE url LIKE \'{}\''.format(table, sql_data['url'])
    result = db_connect().query(sql)
    if result:
        record = db_connect().fetch_one()
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
        sql_data = {
            'pid': i,
            'url': url_argv_base.replace('****', str(i)),
            'is_crawed': 0,
            'retry': 3,
        }
        db_connect().insert(table, sql_data)
        db_connect().commit()
        sql = 'SELECT id, pid, url, is_crawed, retry FROM `{}` WHERE url LIKE \'{}\''.format(table, sql_data['url'])
        result = db_connect().query(sql)
        if result:
            record = db_connect().fetch_one()
            url_recode = {
                'id': record[0],
                'pid': record[1],
                'url': record[2],
                'is_crawed': record[3],
                'retry': record[4]
            }
            response = url_craw.craw(url_recode=url_recode)
            url_analyse.id_spider_analyse(table=table, response=response)