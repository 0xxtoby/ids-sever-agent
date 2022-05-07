# PcapAudit类
import os
import socket

import scapy.all as scapy
import scapy_http.http
import toml

import dpkt

from api.src.AlarmInfo import  AlertInfo
from api.util import match_rule, match_rule_str
class pcp:
    def __init__(self):
        self.src_ip = ""
        self.dst_ip = ""
        self.src_port = 0
        self.dst_port = 0
        self.proto = ""
        self.data = ""
        self.http_obj = ""
        self.http_obj_str = ""
        self.type = ""
        self.timestamp = 0
        self.str=""
        self.domain_name=""
        self.response_ip=""
    def get_dict(self):
        return {
            "src_ip": self.src_ip,
            "dst_ip": self.dst_ip,
            "src_port": self.src_port,
            "dst_port": self.dst_port,
            "proto": self.proto,
            "data": self.data,
            "http_obj": self.http_obj,
            "http_obj_str": self.http_obj_str,
            "type": self.type,
            "timestamp": self.timestamp,
            "str": self.str,
            "domain_name":self.domain_name,
            "response_ip":self.response_ip
        }
        # dict['src'] = socket.inet_ntoa(ip.src)  # 源ip
        # dict['dst'] = socket.inet_ntoa(ip.dst)  # 目的ip
        # dict['src_port'] = src_port  # 源端口
        # dict['dst_port'] = des_port  # 目的端口
        # dict['protocol'] = "udp"  # 协议
        # dict['domain_name'] = domain_name  # 域名
        # dict['response_ip'] = response_ip  # dns返回ip
        # dict['type'] = "dns"  # 协议类型
        # dict['timestamp'] = timestamp  # 时间戳
        # dict['str'] = str(dns)  # 打印字符串
        #


class PcapAudit:
    app_pcap_list = []
    ip_rules = []
    rules = []
    cfg = toml.load('./api/ids.toml')

    def __init__(self, pcap_data):
        PcapAudit.app_pcap_list = []
        PcapAudit.ip_rules = []
        PcapAudit.rules = []
        self.read_rules()
        self.F=0
        self.pcap = pcap_data

    # 获取pcap文件中的数据包
    def parse_pcap(self, ):
        pcap = self.pcap
        ip_data_data=b''
        for timestamp, buffer in pcap:
            dict = {}
            ethernet = dpkt.ethernet.Ethernet(buffer)
            # 判断是空包
            if not isinstance(ethernet.data, dpkt.ip.IP):
                continue
            ip = ethernet.data

            # 解析dns包

            if isinstance(ip.data, dpkt.udp.UDP):
                udp = ip.data
                if len(udp.data) == 0:
                    continue
                dns = udp.data
                # print(ip.p)

                src_port = udp.sport  # 源端口
                des_port = udp.dport  # 目的端口

                if des_port != 53 and src_port != 53:  # 判断是否是dns协议
                    continue
                try:
                    dns = dpkt.dns.DNS(udp.data)
                    domain_name = dns.qd[0].name  # 域名
                except:
                    continue

                try:
                    response_ip = socket.inet_ntoa(dns.an[0].ip)  # dns返回ip
                except:
                    response_ip = ""  # dns请求，则没有ip返回

                dict['src'] = socket.inet_ntoa(ip.src)  # 源ip
                dict['dst'] = socket.inet_ntoa(ip.dst)  # 目的ip
                dict['src_port'] = src_port  # 源端口
                dict['dst_port'] = des_port  # 目的端口
                dict['protocol'] = "udp"  # 协议
                dict['domain_name'] = domain_name  # 域名
                dict['response_ip'] = response_ip  # dns返回ip
                dict['type'] = "dns"  # 协议类型
                dict['timestamp'] = timestamp  # 时间戳
                dict['str'] = str(dns)  # 打印字符串

                PcapAudit.app_pcap_list.append(dict)

            elif ip.p == 6:
                tcp = ip.data
                # 过滤掉内容为空的包
                if len(tcp.data) == 0:
                    continue
                # 5元组
                byteArray = tcp.data

                # print(6)
                dict['src'] = socket.inet_ntoa(ip.src)
                dict['src_port'] = tcp.sport
                dict['dst'] = socket.inet_ntoa(ip.dst)
                dict['dst_port'] = tcp.dport
                dict['protocol'] = "tcp"
                dict['type'] = ""
                if byteArray[0:4] == b'GET ':
                    try:
                        http = dpkt.http.Request(tcp.data)
                        dict['http'] =http
                    except:
                        pass

                    dict['type'] = 'GET'
                    try:
                        dict['str'] = tcp.data.decode("utf-8")
                    except:
                        dict['str'] = str(tcp.data)
                elif byteArray[0:4] == b'HTTP':
                    try:
                        Response = dpkt.http.Response(byteArray)
                        dict['http'] = Response
                    except:
                        pass
                    dict["type"] = "response"

                    try:
                        dict['str'] = tcp.data.decode("uft-8")
                    except:
                        dict['str'] = str(tcp.data)
                # 判断是否为DNS请求
                else:

                    if byteArray[0:4] == b'POST':
                        dict['type'] = 'post'

                        dict['str'] = tcp.data.decode("utf-8")
                        self.F=1
                    elif self.F==1:
                        dict['type'] = 'post_data'
                        try:
                            dict['str'] = tcp.data.decode("utf-8")
                        except:
                            dict['str'] = str(tcp.data)

                # 判断是否为HTTP响应
                dict['timestamp'] = timestamp

                PcapAudit.app_pcap_list.append(dict)

    # 读取规则文件
    def read_rules(self):
        with open(self.cfg['rules_file'], 'r') as f:
            text = f.read()
        RF = 0
        for line in text.split('\n'):
            if RF == 0:
                RF = 1
                dic = {}
                rules = []
                dic['rule_name'] = line
            elif line and line.strip() != '':
                rules.append(line.strip())
            else:
                dic['rules'] = rules
                PcapAudit.rules.append(dic)
                RF = 0

        with open(self.cfg['ip_rules_file'], 'r') as f:
            text = f.read()
        RF = 0
        for line in text.split('\n'):
            if RF == 0:
                RF = 1
                dic = {}
                rules = []
                dic['rule_name'] = line
            elif line and line.strip() != '':
                rules.append(line.strip())
            else:
                dic['rules'] = rules
                PcapAudit.ip_rules.append(dic)
                RF = 0

    def alert(self, alert_info,info_list=[]):
        with open(self.cfg['agent_log'], 'a', encoding='utf-8') as f:
            f.write(alert_info)
            f.write('\n')
        # info_list = [i['src'], i['src_port'], i['dst'], i['dst_port'], i['str'], rule,rules_dic['rule_name'],i['timestamp']]
        alert_obj=AlertInfo()

        alert_obj.alrm_type="pcap扫描检测"
        alert_obj.src_ip=info_list[0]
        alert_obj.src_port=info_list[1]
        alert_obj.dst_ip=info_list[2]
        alert_obj.dst_port=info_list[3]
        alert_obj.proto_data = info_list[4]
        alert_obj.alrm_rule=info_list[5]
        alert_obj.alrm_rule_name=info_list[6]
        alert_obj.alrm_time=info_list[7]
        alert_obj.save_aler()



    def pcap_check(self):
        self.parse_pcap()
        for i in PcapAudit.app_pcap_list:
            if i['protocol'] == "udp":
                if i['type'] == 'dns':
                    for ip_rule_dic in PcapAudit.ip_rules:
                        for ip_rule in ip_rule_dic['rules']:
                            if ip_rule in i['str'] or \
                                    ip_rule == i['domain_name'] or \
                                    ip_rule == i['response_ip'] or \
                                    ip_rule == i['src'] or \
                                    ip_rule == i['dst']:
                                alert_info = "| {} | [+]检测到威胁 {}->{} 域名:{} 解析目的IP:{}".format(
                                    ip_rule_dic['rule_name'], i['src'], i['dst'], i['domain_name'], i['response_ip'])
                                info_list = [i['src'],'', i['dst'], '', i['str'], ip_rule,ip_rule_dic['rule_name'], i['timestamp']]
                                print(alert_info)
                                self.alert(alert_info,info_list)
            elif i['protocol'] == 'tcp':
                wwww=0
                for rules_dic in PcapAudit.rules:
                    for rule in rules_dic['rules']:

                        if "http" in i.keys() and i['type'] != "response":
                            if match_rule_str(i['http'].uri, rule) :
                                alert_info = "| {} | [+]检测到威胁 {}->{} {}".format(
                                    rules_dic['rule_name'], i['src'], i['dst'], i['http'].uri)
                                print(alert_info)
                                info_list = [i['src'], i['src_port'], i['dst'], i['dst_port'], i['str'], rule,
                                             rules_dic['rule_name'], i['timestamp']]
                                self.alert(alert_info,info_list)
                            if match_rule_str(i['str'], rule):
                                alert_info = "| {} | [+]检测到威胁 {}->{} {} {}".format(
                                    rules_dic['rule_name'], i['src'], i['dst'], i['str'].find(rule), rule)
                                info_list = [i['src'], i['src_port'], i['dst'], i['dst_port'], i['str'], rule,
                                             rules_dic['rule_name'], i['timestamp']]
                                print(alert_info)
                                self.alert(alert_info, info_list=info_list)
                        elif i['type'] == "post" or i['type'] == "post_data":
                            if match_rule_str(i['str'], rule) and rules_dic['rule_name'] != "sql注入":

                                alert_info = "| {} | [+]检测到威胁 {}->{} {} {}".format(
                                        rules_dic['rule_name'], i['src'], i['dst'], i['str'].find(rule), rule)
                                info_list = [i['src'], i['src_port'], i['dst'], i['dst_port'], i['str'], rule,
                                             rules_dic['rule_name'], i['timestamp']]
                                print(alert_info)
                                self.alert(alert_info,info_list=info_list)



if __name__ == '__main__':
    # packets = scapy.rdpcap("./api/data/bingxie.pcap")
    # for p in packets:
    #     p.show()

    #读取文件夹
    for root, dirs, files in os.walk("./api/data/pcap"):
        for file in files:
            if file.endswith(".pcap"):
                print(os.path.join(root, file))
                with open(os.path.join(root, file), "rb") as f:
                    pcap = dpkt.pcap.Reader(f)
                    a = PcapAudit(pcap)
                    # print(a.rules)
                    a.pcap_check()

