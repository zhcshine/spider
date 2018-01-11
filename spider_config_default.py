# -*- encoding: utf8 -*-
def spider_config():
    config = {
        # 设置超时时长
        'timeout': 10,
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
        # 过滤包含相关路径的url,　例如search, chaxun等搜索相关
        'filter_path': [],
        # utf-8/gbk
        'decode': '',
        'retry': 3
    }
    return config