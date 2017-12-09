# -*- encoding: utf8 -*-
class SpiderPrint:
    def __init__(self):
        pass

    def print_spending_time(self, method_str, spending_time):
        print u"%+10s %-20s" % (method_str, spending_time)

    def print_error_msg(self, msg):
        print u"\033%s" % (msg)

    def print_line(self, msg):
        print u"%-25s" % (msg * 40)

    def print_msg(self, msg):
        print u"%s" % (msg)

def main():
        print u"请传入数据库配置信息"

if __name__ == '__main__':
    main()