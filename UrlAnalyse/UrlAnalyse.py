# -*- encoding: utf8 -*-
import sys
import urlparse
import MySQLdb
sys.path.append('..')
reload(sys)
from bs4 import BeautifulSoup
sys.setdefaultencoding("utf-8")


class UrlAnalyse:
    def __init__(self, db, config):
        self.db = db
        self.config = config

    def analyse(self, table, base_url, response):
        id = response['id']
        code = response['code']
        retry = response['retry']
        html = response['html']
        try:
            if code == 200 or code == 304:
                # 查询需要的urls列表
                new_urls = self.get_urls(html, base_url)
                # 判断是否重复，重复则丢弃，不重复则写入数据库
                for new_url in new_urls:
                    sql = 'SELECT id, url FROM {} WHERE url = \'{}\''.format(table, new_url)
                    results = self.db.query(sql)
                    if results == 0:
                        sql_data = {
                            'pid': id,
                            'url': new_url,
                            'is_crawed': 0,
                            'retry': self.config['retry'],
                        }
                        self.db.insert(table, sql_data)
                        self.db.commit()
                try:
                    decode_code = self.config['decode']
                    if decode_code == '':
                        html = html.encode('utf-8')
                    else:
                        html = html.decode(decode_code).encode('utf-8')
                    html_escaped = MySQLdb.escape_string(self.pretty_html(html))
                except:
                    html_escaped = html
                sql_data = {
                    'is_crawed': 1,
                    'code': code,
                    'html': html_escaped
                }
            elif code == 404:
                sql_data = {
                    'is_crawed': 1,
                    'code': code,
                    'html': html
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
            self.db.update(table, sql_data, condition)
            self.db.commit()
        except Exception, e:
            sql_data = {
                'is_crawed': 1,
                'code': code,
                'html': 'analyseError'  # str(e)
            }
            condition = 'id = {}'.format(id)
            self.db.update(table, sql_data, condition)
            self.db.commit()

    def id_spider_analyse(self, table, response):
        id = response['id']
        code = response['code']
        html = response['html']
        try:
            html_escaped = MySQLdb.escape_string(self.pretty_html(html.encode('utf-8')))
        except:
            html_escaped = html
        sql_data = {
            'is_crawed': 1,
            'code': code,
            'html': html_escaped
        }
        condition = 'id = {}'.format(id)
        try:
            self.db.update(table, sql_data, condition)
            self.db.commit()
        except Exception, e:
            sql_data = {
                'is_crawed': 1,
                'code': 800,
                'html': 'analyseError'  # str(e)
            }
            condition = 'id = {}'.format(id)
            self.db.update(table, sql_data, condition)
            self.db.commit()


    def get_urls(self, html, base_url):
        bs_obj = BeautifulSoup(html, 'html.parser', from_encoding='utf8')
        urls_list = bs_obj.find_all(name='a')
        needed_urls = []
        for url in urls_list:
            try:
                url = url['href']
                print url
                # 删除有Javascript的链接
                if 'javascript' in str(url):
                    continue

                # 如果是以/开头的url，则此url是需要爬取的url
                spider_config = self.config
                filter_params = spider_config['filter_params']
                filter_query = spider_config['filter_query']
                href = self.url_filter(url, filter_params=filter_params, filter_query=filter_query)
                url_parse = urlparse.urlparse(href)
                if not url_parse.netloc:
                    needed_urls.append(base_url + '/' + href.lstrip('/'))
                else:
                    if url_parse.scheme:
                        new_base_url = url_parse.scheme + '://' + url_parse.netloc
                        if new_base_url == base_url:
                            needed_urls.append(href)
                    else:
                        new_base_url = 'http://' + url_parse.netloc
                        if new_base_url == base_url:
                            needed_urls.append(href)
            except:
                pass
        return needed_urls

    # 优化html文件
    def pretty_html(self, html):
        bs_obj = BeautifulSoup(html, 'html.parser', from_encoding='utf8')
        pretty_html = bs_obj.prettify()
        return pretty_html

    # 过滤url的输入参数
    def url_filter(self, url, filter_params, filter_query):
        url_parse = urlparse.urlparse(url)
        url_scheme = url_parse.scheme
        url_netloc = url_parse.netloc
        url_path = url_parse.path
        url_params = url_parse.params
        url_query = url_parse.query
        url_fragment = url_parse.fragment
        # 删除指定输入参数
        url_params_list = url_params.split(';')
        for params in filter_params:
            for url_params in url_params_list:
                url_params_list_list = url_params.split('=')
                if params in url_params_list_list:
                    url_params_list.remove(url_params)
        new_url_params = ';'.join(url_params_list)
        # 删除指定查询参数
        url_query_list = url_query.split('&')
        for query in filter_query:
            for url_query in url_query_list:
                url_query_list_list = url_query.split('=')
                if query in url_query_list_list:
                    url_query_list.remove(url_query)
        new_url_query = '&'.join(url_query_list)
        new_url = urlparse.urlunparse((url_scheme, url_netloc, url_path, new_url_params, new_url_query, ''))
        return new_url

    # 


def main():
    print u"请传入一条数据库数据"


if __name__ == '__main__':
    main()