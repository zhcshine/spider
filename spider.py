# -*- encoding: utf8 -*-
import sys
from spider_config import spider_config
from Initialization import Initialization
from UrlManager import UrlManager
from UrlCraw import UrlCraw
from UrlAnalyse import UrlAnalyse
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

""" 初始化爬虫 """
# 获取简易版url，去除参数，去除http，https
url_argv = sys.argv[1]
initialization = Initialization.Initialization(url_argv)
base_url = initialization.initialization_url()
table = initialization.initialization_create_table(base_url)
# 是否设置代理
spider_config = spider_config()
proxy = spider_config['proxy']

""" 引入调度器，爬取器，分析器"""
has_craw_url = UrlManager.UrlManager()
url_manager = UrlManager.UrlManager()
url_craw = UrlCraw.UrlCraw()
url_analyse = UrlAnalyse.UrlAnalyse()

""" 开始循环爬取 """
while has_craw_url.has_craw_url(table=table):
    print u'************************************'
    time_begin = datetime.datetime.now()
    url_recode = url_manager.get_one_url(table=table)
    time_end_manager = datetime.datetime.now()
    excute_time = (time_end_manager - time_begin).seconds
    print u'调度器耗时： ' + str(excute_time) + 's'

    response = url_craw.craw(url_recode=url_recode)
    time_end_craw = datetime.datetime.now()
    excute_time = (time_end_craw - time_end_manager).seconds
    print u'爬取器耗时： ' + str(excute_time) + 's'

    url_analyse.analyse(table=table, base_url=base_url, response=response)
    time_end_analyse = datetime.datetime.now()
    excute_time = (time_end_analyse - time_end_craw).seconds
    print u'分析器耗时： ' + str(excute_time) + 's'