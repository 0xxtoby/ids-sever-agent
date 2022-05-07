import json
import random
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from api.src.AlarmInfo import AlarmInfo_list
from api.src.control_center  import ControlCenter
from api.src.log_emp import LogAnalyze


class ServerJsonMsg(object):
    def __init__(self, status, msg, len=0, data=''):
        self.status = status
        self.msg = msg
        self.data = data
        self.len = len
        self.json = {
            'status': self.status,
            'msg': self.msg,
            'data': self.data,
            'len':self.len
        }
    def __str__(self):
        #返回json
        return self.json
    #返回json




data={
    'name':'',
    'ip':'',
    'port':'',
    'data':'',
    'type':'',
    'id':'',
    'system':'',
    'datetime':'',

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

def agent_msg_emp(request):
    f_no=0
    if request.method == 'POST':

        if request.POST['type'] in "1,2,3,4,5" :

            yield ServerJsonMsg(200, '接受成功' ,len(request.POST)).json

            ControlCenter(request).process()

            #将data存入队列

        else:
            #接受失败
            yield ServerJsonMsg(400, '接受失败').json
    else:
        #接受失败
        yield ServerJsonMsg(400, '接受失败').json

#接受信息
def agent_msg(request):
    json=agent_msg_emp(request)

    return HttpResponse(json)


