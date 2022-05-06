from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from myApp.DAO.lianjia import lianjia_emp
from myApp.DAO.qax import qax_emp
from myApp.DAO.qax2 import qax2_emp
from myApp.DAO.reebuf import reebuf_emp


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
            path = request.GET.get("next") or "/lianjia"
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








