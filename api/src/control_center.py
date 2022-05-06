
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

        if (self.type == '1' or self.type == '2'):
            ff = request.FILES['file']
            dd = b''
            for chunk in ff.chunks():
                dd += chunk

            self.DD['data'] = str(dd, encoding ="utf-8")

            self.loganalyze=LogAnalyze()
            self.loganalyze.set_data(self.DD)
            self.loganalyze.parse_data()
        elif self.type == '3' :
            ff = request.FILES['file']

            with open('./api/file/' + self.DD['f_no'], 'wb') as fff:
                fff.write(b"")

            with open('./api/file/' + self.DD['f_no'], 'wb+') as destination:
                for chunk in ff.chunks():
                    destination.write(chunk)

            with open('./api/file/'+self.DD['f_no'], 'rb') as f:

                pcap = dpkt.pcap.Reader(f)
                aw = PcapAudit(pcap)
                aw.pcap_check()
        elif self.type == '4' :
            ff = request.FILES['file']
            dd = b''
            for chunk in ff.chunks():
                dd += chunk
            with open("ad","wb") as f:
                f.write(dd)
            self.DD['data'] = str(dd, encoding="utf-8")
            authlog=AuthLogs(dd.decode("utf-8"))
            authlog.ssh_brute()



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