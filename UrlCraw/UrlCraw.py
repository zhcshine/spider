# -*- encoding: utf8 -*-
import sys
import cookielib
import urllib2
sys.path.append('..')
reload(sys)
sys.setdefaultencoding("utf-8")

class UrlCraw:
    def __init__(self, proxy):
        self.proxy = proxy
        pass

    def get_agent(self):
        agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36';
        return agent

    def craw(self, url_recode):
        id = url_recode['id']
        pid = url_recode['pid']
        url = url_recode['url']
        retry = url_recode['retry']
        proxy = self.proxy
        if proxy['type'] == 'socks5':
            import socks
            import socket
            socks.set_default_proxy(socks.SOCKS5, proxy['host'], int(proxy['port']))
            socket.socket = socks.socksocket
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        accessed_url = urllib2.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        print accessed_url
        request = urllib2.Request(accessed_url)
        request.add_header('user-agent', self.get_agent())
        try:
            response = urllib2.urlopen(request)
            response_result = {
                'id': id,
                'pid': pid,
                'url': url,
                'code': response.getcode(),
                'retry': retry,
                'html': response.read()
            }
            return response_result
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
