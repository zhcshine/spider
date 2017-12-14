# -*- encoding: utf8 -*-
def spider_config():
    config = {
        # 设置超时时长
        'timeout': 120,
        # 代理设置
        'proxy': {
            'type': '',
            'host': '',
            'port': '',
            'user': '',
            'password': '',
        },
        # 'proxy': {
        #     'type': 'socks5',
        #     'host': '127.0.0.1',
        #     'port': '1080',
        #     'user': '',
        #     'password': '',
        # },
        # 过滤url输入参数
        'filter_params': ['jsessionid', ],
        # 过滤url查询参数
        'filter_query': [],
        # 目标网站的编码
        'decode': 'gbk',
        # 设置重复次数
        'retry': 2
    }
    return config