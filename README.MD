### 简易爬取指定网站的全部内容


### 环境
> mysql
> python2.7

### 安装
```
git cloud https://github.com/zhcshine/spider.git
# -p参数为指定的python版本，根据自己实际情况进行选择
virtualenv --no-site-packages -p /usr/local/bin/python .
pip install -r requirements.txt
```
```
将db_config_default.py 改成db_config.py并配置相关信息
将spider_config_default.py 改成spider_config.py并配置相关信息
```
### 运行
```
python spider.py http://www.***.com
```
### 错误提示
```
SSLError: [Errno 1] _ssl.c:510: error:14077438:SSL routines:SSL23_GET_SERVER_HELLO:tlsv1
```
将python版本升级到python2.7.9


#### 待更新：
user-agent
cookie