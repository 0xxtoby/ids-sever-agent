import os
from pprint import pprint


class system_info:
    def __init__(self):
        self.os = os.name
        self.platform = os.sys.platform #系统类型
        self.architecture = os.uname().machine#系统架构
        self.hostname = os.uname().nodename#主机名
        self.release = os.uname().release#发行版本
        self.version = os.uname().version#版本
        self.machine = os.uname().machine#机器

        self.python_version = os.sys.version#python版本
        self.mysql_version = os.popen('mysql -V').read()#mysql版本


    def __str__(self):
        return "os:%s\nplatform:%s\narchitecture:%s\nhostname:%s\nrelease:%s\nversion:%s\nmachine:%s\npython_version:%s\nmysql_version:%s"%(self.os,self.platform,self.architecture,self.hostname,self.release,self.version,self.machine,self.python_version,self.mysql_version)

    def get_list(self):
        return [["系统类型",self.os],["系统类型",self.platform],["系统架构",self.architecture],["主机名",self.hostname],["发行版本",self.release],["版本",self.version],["机器",self.machine],["python版本",self.python_version],["mysql版本",self.mysql_version]]

if __name__ == '__main__':
    pprint(system_info().get_list())

