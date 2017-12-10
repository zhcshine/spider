# -*- encoding: utf8 -*-
import sys
import db_config
import spider_config
from DbManager import DbManager
from Initialization import Initialization
from UrlManager import UrlManager
from UrlCraw import UrlCraw
from UrlAnalyse import UrlAnalyse
from SpiderPrint import SpiderPrint
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")


class Spider:
    def __init__(self, url_argv):
        sys.setrecursionlimit(10000000)
        """ 调度数据库接口, 引入初始化, 调度器, 爬取器, 分析器 """
        self.db = DbManager.DbManager(db_config).mysql_connect()
        self.config = spider_config.spider_config()
        self.initialization = Initialization.Initialization(self.db, self.config, url_argv)
        self.manager = UrlManager.UrlManager(self.db, self.config)
        self.craw = UrlCraw.UrlCraw(self.db, self.config)
        self.analyse = UrlAnalyse.UrlAnalyse(self.db, self.config)
        self.sprint = SpiderPrint.SpiderPrint()
        self.initialize_spider()
    """ 初始化爬虫 """
    # 获取简易版url，去除参数，去除http，https
    def initialize_spider(self):
        self.sprint.print_line('*')
        self.sprint.print_msg('正在初始化爬虫')
        # 获取基础url地址，例如https://www.baidu.com
        self.base_url = self.initialization.initialization_url()
        self.sprint.print_msg('爬取网站地址：' + self.base_url)
        # 根据基础url地址生成数据库表
        self.table = self.initialization.initialization_create_table(self.base_url)
        self.sprint.print_msg('生成数据库表：' + self.table)
        self.sprint.print_line('*')

    def time_difference(self, begin_time, end_time):
        return float((end_time - begin_time).microseconds) / (1000 * 1000)

    def get_spider_url(self):
        time_begin_manager = datetime.datetime.now()
        url_recode = self.manager.get_one_url(table=self.table)
        time_end_manager = datetime.datetime.now()
        excute_time_manager = self.time_difference(time_begin_manager, time_end_manager)
        self.sprint.print_spending_time('MangerUrl：', str(excute_time_manager) + 's')
        return url_recode

    def craw_spider_url(self, url):
        time_begin_craw = datetime.datetime.now()
        response = self.craw.craw(url_recode=url)
        time_end_craw = datetime.datetime.now()
        excute_time_craw = self.time_difference(time_begin_craw, time_end_craw)
        self.sprint.print_spending_time('CrawUrl：', str(excute_time_craw) + 's')
        return response

    def analyse_spider_result(self, response):
        time_begin_analyse = datetime.datetime.now()
        self.analyse.analyse(table=self.table, base_url=self.base_url, response=response)
        time_end_analyse = datetime.datetime.now()
        excute_time_analyse = self.time_difference(time_end_analyse, time_begin_analyse)
        self.sprint.print_spending_time('Analyse：', str(excute_time_analyse) + 's')

    def spider(self):
        url_recode = self.get_spider_url()
        response = self.craw_spider_url(url_recode)
        self.analyse_spider_result(response)
        self.sprint.print_line('*')
        Spider.spider(self)

url_argv = sys.argv[1]
spider = Spider(url_argv)
spider.spider()