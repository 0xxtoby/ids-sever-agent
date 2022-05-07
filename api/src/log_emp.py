import re
import socket
import time
from pprint import pprint

import dpkt as dpkt
import toml

from api.src.AlarmInfo import AlertInfo
from api.util import match_rule

data = {
    'name': '',
    'ip': '',
    'port': '',
    'data': '',
    'type': '',
    'id': '',
    'system': '',
    'datetime': '',

}
agent_system_dict = {
    '1': 'windows',
    '2': 'linux',
    '3': 'mac',
    '4': 'other',

}
agent_type_dict = {
    '1': 'apache',
    '2': 'nginx',
    '3': 'pcap',
    '4': 'windowslog',
    '5': 'linuxlog',
}

#agent类
class LogAnalyze:
    toml_file = "./api/ids.toml"
    cfg = toml.load(toml_file)

    access_list = []
    alert_info = ''
    alert_list = []
    rule_list = []
    rule_dict = {}

    def __int__(self):
        LogAnalyze,access_list = []
        LogAnalyze.alert_info = ''
        LogAnalyze.alert_list = []
        LogAnalyze.rule_list = []
        LogAnalyze.rule_dict = {}


    def set_data(self, data):
        self.name = data['name']
        self.ip = data['ip']
        self.port = data['port']
        self.data = data['data']
        self.type = data['type']
        self.id = data['id']
        self.system = data['system']
        self.datetime = data['datetime']

    def http_dict(self):
        http_dic={}



    def log_line_dict(self,access_line):
        access_dict = {}
        access_dict['ip'] = access_line.split(' ')[0]
        access_dict['time'] = access_line.split(' ')[3]
        access_dict['method'] = access_line.split(' ')[5]
        access_dict['url'] = access_line.split(' ')[6]
        access_dict['protocol'] = access_line.split(' ')[7]
        access_dict['status'] = access_line.split(' ')[8]
        access_dict['size'] = access_line.split(' ')[9]
        return access_dict

    #读取规则文件
    def read_rules(self):
        with open(self.cfg['rules_file'], 'r') as f:
            text = f.read()

        F = 0
        for line in text.split('\n'):
            if F == 0:
                F = 1
                dic = {}
                rules = []
                dic['rule_name'] = line
            elif line and line.strip() != '':
                rules.append(line.strip())

            else:
                dic['rules'] = rules
                LogAnalyze.rule_list.append(dic)
                F = 0

    def alert(self,alert_info,info_list=[]):
        with open(self.cfg['agent_log'], 'a', encoding='utf-8') as f:
            f.write(alert_info)
            f.write('\n')
    #     info_list=[ip, time,method,url,protocol,status,size,rule_name,rule]
        Aler=AlertInfo()

        Aler.dst_ip = info_list[0]
        Aler.alrm_time= time.mktime(time.strptime(info_list[1][1:20], "%d/%b/%Y:%H:%M:%S"))
        Aler.alrm_type = 'web_日志检测'
        Aler.proto_data = "{}{} {} {} {} {} {} {}".format(info_list[0],info_list[1],info_list[2],info_list[3],info_list[4],info_list[5],info_list[6],info_list[7],info_list[8])
        Aler.alrm_rule = info_list[8]
        Aler.alrm_rule_name = info_list[7]
        Aler.save_aler()






    # log检测
    def log_check(self):
        self.read_rules()#读取规则文件

        for line in self.access_list:
            for rule in self.rule_list:
                rule_name = rule['rule_name']
                rules = rule['rules']
                for i in rules:
                    # 判断rule是否在line中
                    if match_rule(line, i):#如果匹配到了规则
                        alert_info = '[+]检测到威胁{ip} {time} {method} {url} {protocol} {status} {size}'.format(**line)
                        print("｜ " + rule_name + " ｜" + alert_info)
                        #告警
                        self.alert("｜ " + rule_name + " ｜" + alert_info,info_list=[line['ip'],line['time'],line['method'],line['url'],line['protocol'],line['status'],line['size'],rule_name,i])

    def list_add(self,data):
        print(self.toml_file)
        self.access_list.append(data)

    def parse_data(self):

        for line in self.data.split('\n'):
                if line and line[0] != '':
                    try:
                        LogAnalyze.access_list.append(self.log_line_dict(line.strip()))
                    except:
                        pass
        self.log_check()




if __name__ == '__main__':
    data = {
        'name': '',
        'ip': '',
        'port': '',
        'data': open('./api/data/nginx.log', 'r', encoding='utf-8').read(),
        'type': '1',
        'id': '',
        'system': '1',
        'datetime': '',

    }
    # print(data)
    a=LogAnalyze()
    a.set_data(data)
    a.parse_data()



