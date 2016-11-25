# -*- encoding: utf8 -*-
def spider_config():
    config = {
        # 代理设置
        'proxy': {
            'type': '',  # 支持socks5
            'host': '',
            'port': '',
            'user': '',
            'password': '',
        },
        # 过滤url输入参数
        'filter_params': [],
        # 过滤url查询参数
        'filter_query': [],
    }
    return config