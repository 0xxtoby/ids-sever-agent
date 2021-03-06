import time

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from api.src.AlarmInfo import AlarmInfo_list
from api.src.system_info import system_info


@csrf_exempt
def login(request):
    if request.method == "GET":
        print("GET")
        context = {}
        # print('reg_error',request.session.reg_error)
        try:
            context['error']=request.session.get('reg_error')
            del request.session['reg_error']
        except:
            print("reg_error错误吧")

        return render(request, "login.html",context)
    username = request.POST.get("username")
    password = request.POST.get("password")
    valid_num = request.POST.get("valid_num")
    keep_str = request.session.get("keep_str")

    if keep_str == valid_num:
        user_obj = auth.authenticate(username=username, password=password)



        if user_obj == None or str(user_obj) == 'AnonymousUser':
            request.session["reg_error"] = '账号密码错误'
            return redirect("/login")
        else:

            auth.login(request, user=user_obj)
            print('登录成功', user_obj)
            path = request.GET.get("next") or "/ids_admin"
            print(path)
            return redirect(path)
    else:
        return redirect("/login")

def index(request):
    if request.user == None or str(request.user) == 'AnonymousUser':
        request.session["reg_error"]='账号密码错误'
        return redirect("/login")
    else:
        print(request.user,)
        return  render(request,"index.html")
def logout(request):
    ppp = auth.logout(request)
    print(ppp) # None
    return redirect("/login")
def register(request):
    dic={}

    if request.method == "GET":
        context={}
        try:
            context['error'] = request.session.get('reg_error')

            del request.session['reg_error']
        except:
            print("reg_error错误吧")
        print("GET")
        return render(request, "register.html",context)
    username = request.POST.get("username")
    password = request.POST.get("password")
    if(password==None):
        request.session["reg_error"] = '密码不能为空'
        return redirect("/register")
    else:
        try:
            user_obj = User.objects.create_user(username=username, password=password)
            print(user_obj)
        except:
            request.session["reg_error"]= '用户注册失败（用户名已存在）'
            return redirect("/register")
    request.session["reg_error"] = '注册成功！'
    return redirect("/login")

def ids_index(request):
    if request.method == "GET":
        context={}
        try:
            context["data"] = request.session.get("data")
            del request.session["data"]
        except:
            print("无data")
        try:
            context["error"] = request.session.get("error")
            del request.session["error"]
        except:
            print("无error")


        ip=request.GET.get("ip","")
        rule=request.GET.get("rule","")
        type=request.GET.get("type","")

        page = int(request.GET.get("page", 1))

        context['rule_list']=AlarmInfo_list().read_rule_name()
        context['type_list']=AlarmInfo_list().read_rule_type()
        context['ip_list']=AlarmInfo_list().read_ip()
        if ip =="" and rule=="" and type=="":
            data=AlarmInfo_list().read_alarm_info(page)
            page_num=AlarmInfo_list().get_page_num()
            prev_page=page-1
            next_page=page+1
            if page < 4:
                page_s = [1, 2, 3, 4, 5]
            elif page > page_num - 3:
                page_s = [page_num - 4, page_num - 3, page_num - 2, page_num - 1, page_num]
            else:
                page_s = [page - 2, page - 1, page, page + 1, page + 2]
            if prev_page<1:
                prev_page=1
            if next_page>page_num:
                next_page=page_num
            context["prev_page"]=prev_page
            context["next_page"]=next_page
            context["data"] = data
            context["page"] = page
            context["page_s"] = page_s
            context["page_num"] = page_num
            return render(request, "order-list1.html",context)

        elif ip !="" or  rule=="" or type=="":
            data,page_num=AlarmInfo_list().read_alarm_info_by_ip_rule_type(ip,rule,type,page)
            prev_page = page - 1
            next_page = page + 1

            if page < 4:
                page_s = [1, 2, 3, 4, 5]
            elif page > page_num - 3:
                page_s = [page_num - 4, page_num - 3, page_num - 2, page_num - 1, page_num]
            else:
                page_s = [page - 2, page - 1, page, page + 1, page + 2]
            if page_num< 5:
                page_s =[]

                for i in range(1,page_num+1):
                    page_s.append(i)

            if prev_page < 1:
                prev_page = 1
            if next_page > page_num:
                next_page = page_num
            context["prev_page"] = prev_page
            context["next_page"] = next_page
            context["data"] = data
            context["page"] = page
            context["page_s"] = page_s
            context["page_num"] = page_num
            context["ip"] = ip
            context["rule"] = rule
            context["type"] = type
            context['page_T']=1

            return render(request, "order-list1.html", context)


#

def order_details(request):
    if request.method == "GET":
        context={}
        id=request.GET.get("id")
        data=AlarmInfo_list().select_id(id)
        context["data"]=data

        return render(request, "order-details.html",context)

def ids_admin(request):
    return render(request, "ids_index.html")

def welcome(request):
    context={}

    sys_info=system_info().get_list()
    context["sys_info"]=sys_info
    alrm_type_num=AlarmInfo_list().get_alrm_type_num()
    rule_name_num=AlarmInfo_list().get_rule_name_num()
    context["alrm_type_num"]=alrm_type_num
    context["rule_name_num"]=rule_name_num
    #后去当前时间
    now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    context['time']=now_time

    return render(request, "welcome.html",context)








