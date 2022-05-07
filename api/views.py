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


# @login_required(login_url='/login')
def ids_alem(request):
    if request.method == "GET":
        context={}
        try:
            context["lianjia_data"] = request.session.get("lianjia_data")
            del request.session["lianjia_data"]
        except:
            print("lianjia_data错误吧")
        try:
            context["error"] = request.session.get("error")
            del request.session["error"]
        except:
            print("无error")

        page = request.GET.get("page", 1)
        data=AlarmInfo_list().read_alarm_info(page)
        context["data"] = data

        return render(request, "lianjia.html",context)




    # # ?dp_no = 0 & fs_no = 0 & zj_no = 0 & hx_no = 0 & cx_no = 0 & pg_no = 55
    # dp_no = request.POST.get("dp_no")
    # fs_no = request.POST.get("fs_no")
    # zj_no = request.POST.get("zj_no")
    # hx_no = request.POST.get("hx_no")
    # cx_no = request.POST.get("cx_no")
    # pg_no = request.POST.get("pg_no")
    # l =lianjia_emp()
    #
    # try:
    #     data_list=l.main(dp_no,fs_no,zj_no,hx_no,cx_no,pg_no)
    # except:
    #     request.session["error"] = "输入错误"
    #     return redirect("/lianjia")
    #
    # # {'content': '1399',
    # #  'des': '仅剩1间/35.00㎡/1间在租/1室1厅1卫',
    # #  'tag_list': ['新上', '独栋公寓', '月租', '有阳台', '开放厨房', '押一付一'],
    # #  'title': '独栋·翔威公寓 飞跃科创园 主路旁边全新公寓 1室1厅'},
    # request.session["lianjia_data"]=data_list
    #
    #
    # return redirect("/lianjia")