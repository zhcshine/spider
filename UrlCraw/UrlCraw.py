# -*- encoding: utf8 -*-
import sys
import cookielib
import urllib2
import spider_config
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")

class UrlCraw:
    def __init__(self, db, config):
        self.db = db
        self.config = config

    def get_agent(self):
        agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36';
        return agent

    def craw(self, url_recode):
        id = url_recode['id']
        pid = url_recode['pid']
        url = url_recode['url']
        retry = url_recode['retry']
        proxy = self.config['proxy']
        timeout = self.config['timeout']
        if proxy['type'] == 'socks5':
            import socks
            import socket
            socks.set_default_proxy(socks.SOCKS5, proxy['host'], int(proxy['port']))
            socket.socket = socks.socksocket
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        accessed_url = urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        request = urllib2.Request(accessed_url)
        request.add_header('user-agent', self.get_agent())
        try:
            response = urllib2.urlopen(request, timeout=timeout)
            response_result = {
                'id': id,
                'pid': pid,
                'url': url,
                'code': response.getcode(),
                'retry': retry,
                'html': response.read()
            }
            return response_result

        except urllib2.HTTPError, e:
            response_result = {
                'id': id,
                'pid': pid,
                'url': url,
                'code': e.getcode(),
                'retry': retry,
                'html': e.read()
            }
            return response_result
        except urllib2.URLError, e:
            response_result = {
                'id': id,
                'pid': pid,
                'url': url,
                'code': 700,  # 自定义700为网络错误
                'retry': retry,
                'html': e
            }
        except Exception, e:
            response_result = {
                'id': id,
                'pid': pid,
                'url': url,
                'code': 700,  # 自定义700为网络错误
                'retry': retry,
                'html': e
            }
            return response_result

def main():
    print u"请传入一条数据库数据"


if __name__ == '__main__':
    main()