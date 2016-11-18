# -*- encoding: utf8 -*-
import sys
import MySQLdb
from mysql_connect import db_connect
from Initialization import Initialization
from UrlManager import UrlManager
from UrlCraw import UrlCraw
from UrlAnalyse import UrlAnalyse
reload(sys)
sys.setdefaultencoding("utf-8")

""" 初始化爬虫 """
# 获取简易版url，去除参数，去除http，https
url_argv = sys.argv[1]
initialization = Initialization.Initialization(url_argv)
base_url = initialization.initialization_url()
table = initialization.initialization_create_table(base_url)

""" 引入调度器，爬取器，分析器"""
url_manager =  UrlManager.UrlManager()
url_craw = UrlCraw.UrlCraw()
url_analyse = UrlAnalyse.UrlAnalyse()

""" 开始循环爬取 """
while url_manager.get_one_url(table=table):
    url_recode = url_manager.get_one_url(table=table)
    response = url_craw.craw(url_recode=url_recode)
    url_analyse.analyse(table=table, base_url=base_url, response=response)