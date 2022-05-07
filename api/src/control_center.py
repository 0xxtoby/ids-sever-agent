
#控制器类
import random
import time

import dpkt

from api.src.ParseLogs import Authlog, AuthLogs
from api.src.log_emp import LogAnalyze

from api.src.pcap_emp import PcapAudit

from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

agent_type_dict = {
    '1': 'apache',
    '2': 'nginx',
    '3': 'pcap',
    '4': 'windowslog',
    '5': 'linuxlog',
}

class ControlCenter:



    def __init__(self,request):
        self.request = request
        post = request.POST


        data = {}

        data['name'] = post['name']
        data['type'] = post['type']
        data['id'] = post['id']
        data['system'] = post['system']
        data['datetime'] = post['datetime']
        data['ip'] = post['ip']
        data['port'] = post['port']


        f_no = str(time.time()) + str(random.randint(0, 10000))
        data['f_no'] = f_no

        self.DD=data
        self.type=data['type']

    #处理
    def process(self):
        request = self.request
        form = UploadFileForm(request.POST, request.FILES)
        #web日志处理
        if (self.type == '1' or self.type == '2'):
            ff = request.FILES['file']
            dd = b''
            for chunk in ff.chunks():
                dd += chunk#
            self.DD['data'] = str(dd, encoding ="utf-8")#转换为字符串
            self.loganalyze=LogAnalyze()#初始化日志分析类
            self.loganalyze.set_data(self.DD)#设置数据
            self.loganalyze.parse_data()#
        #pcap处理
        elif self.type == '3' :
            ff = request.FILES['file']
            with open('./api/file/' + self.DD['f_no'], 'wb') as fff:#清空文件保存文件
                fff.write(b"")

            with open('./api/file/' + self.DD['f_no'], 'wb+') as destination:#保存文件
                for chunk in ff.chunks():
                    destination.write(chunk)

            with open('./api/file/'+self.DD['f_no'], 'rb') as f:#打开文件

                pcap = dpkt.pcap.Reader(f)#读取pcap文件
                aw = PcapAudit(pcap)#初始化pcap分析类
                aw.pcap_check()#分析pcap文件
        #w系统日志处理
        elif self.type == '4' :
            ff = request.FILES['file']
            dd = b''
            for chunk in ff.chunks():
                dd += chunk

            self.DD['data'] = str(dd, encoding="utf-8")
            authlog=AuthLogs(dd.decode("utf-8"))#初始化日志分析类
            authlog.ssh_brute()#分析日志



if __name__ == '__main__':
    data = {
        'name': '',
        'ip': '',
        'port': '',
        'data': open('./api/data/sql注入.pcap', 'rb').read(),
        'type': '3',
        'id': '',
        'system': '1',
        'datetime': '',

    }
    a=ControlCenter(data)
    a.process()