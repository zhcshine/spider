# -*- encoding: utf8 -*-
import sys
import MySQLdb
from mysql_connect import db_connect
from urlparse import urlparse
sys.path.append('..')
reload(sys)
from bs4 import BeautifulSoup
sys.setdefaultencoding("utf-8")


class UrlAnalyse:
    def __init__(self):
        pass

    def analyse(self, table, base_url, response):
        id = response['id']
        pid = response['pid']
        url = response['url']
        code = response['code']
        retry = response['retry']
        html = response['html']
        if code == 200 or code == 304:
            # 查询需要的urls列表
            new_urls = self.get_urls(html, base_url)
            # 判断是否重复，重复则丢弃，不重复则写入数据库
            for new_url in new_urls:
                sql = 'SELECT id, url FROM {} WHERE url LIKE \'{}\''.format(table, new_url)
                results = db_connect().query(sql)
                if results == 0:
                    sql_data = {
                        'pid': id,
                        'url': new_url,
                        'is_crawed': 0,
                        'retry': 5,
                    }
                    db_connect().insert(table, sql_data)
                    db_connect().commit()
            html_escaped = MySQLdb.escape_string(html.encode('utf-8'))
            sql_data = {
                'is_crawed': 1,
                'code': code,
                'html': html_escaped
            }
        else:
            if int(retry) > 1:
                sql_data = {
                    'is_crawed': 0,
                    'retry': retry -1,
                    'code': code,
                    'html': html
                }
            else:
                sql_data = {
                    'is_crawed': 1,
                    'retry': 0,
                    'code': code,
                    'html': html
                }
        condition = 'id = {}'.format(id)
        db_connect().update(table, sql_data, condition)
        db_connect().commit()

    def get_urls(self, html, base_url):
        bs_obj = BeautifulSoup(html, 'html.parser', from_encoding='utf8')
        urls_list = bs_obj.find_all(name='a')
        needed_urls = []
        for url in urls_list:
            try:
                url = url['href']
                # 如果是以/开头的url，则此url是需要爬取的url
                if url[0:1] == '/':
                    needed_urls.append(base_url + url)
                else:
                    href = url.lower()
                    url_parse = urlparse(href)
                    if url_parse.scheme:
                        new_base_url = url_parse.scheme + '://' + url_parse.netloc
                    else:
                        new_base_url = 'http://' + url_parse.netloc
                    if new_base_url == base_url:
                        needed_urls.append(base_url + href)
            except:
                pass
        return needed_urls





