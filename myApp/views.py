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

@login_required(login_url='/login')
def lianjia(request):
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
        return render(request, "lianjia.html",context)

    # ?dp_no = 0 & fs_no = 0 & zj_no = 0 & hx_no = 0 & cx_no = 0 & pg_no = 55
    dp_no = request.POST.get("dp_no")
    fs_no = request.POST.get("fs_no")
    zj_no = request.POST.get("zj_no")
    hx_no = request.POST.get("hx_no")
    cx_no = request.POST.get("cx_no")
    pg_no = request.POST.get("pg_no")
    l =lianjia_emp()

    try:
        data_list=l.main(dp_no,fs_no,zj_no,hx_no,cx_no,pg_no)
    except:
        request.session["error"] = "输入错误"
        return redirect("/lianjia")

    # {'content': '1399',
    #  'des': '仅剩1间/35.00㎡/1间在租/1室1厅1卫',
    #  'tag_list': ['新上', '独栋公寓', '月租', '有阳台', '开放厨房', '押一付一'],
    #  'title': '独栋·翔威公寓 飞跃科创园 主路旁边全新公寓 1室1厅'},
    request.session["lianjia_data"]=data_list


    return redirect("/lianjia")



@login_required(login_url='/login')
def qax(request):
    if request.method == "GET":
        context={}
        try:
            context["qax"] = request.session.get("qax_data")
            del request.session["qax_data"]
        except:
            print("lianjia_data错误吧")
        try:
            context["error"] = request.session.get("error")
            del request.session["error"]
        except:
            print("无error")
        return render(request, "qax.html",context)

    select = request.POST.get("select")
    print(select)
    qa =qax_emp()

    if select == None or select=='':

        request.session["error"] = "输入不能为空"
        return redirect("/qax")

    # {'content': '1399',
    #  'des': '仅剩1间/35.00㎡/1间在租/1室1厅1卫',
    #  'tag_list': ['新上', '独栋公寓', '月租', '有阳台', '开放厨房', '押一付一'],
    #  'title': '独栋·翔威公寓 飞跃科创园 主路旁边全新公寓 1室1厅'},
    data = qa.get_item(select)
    request.session["qax_data"] = data

    return redirect("/qax")

@login_required(login_url='/login')
def qax2(request):
    if request.method == "GET":
        context={}
        try:
            context["qax"] = request.session.get("qax_data")
            del request.session["qax_data"]
        except:
            print("lianjia_data错误吧")
        try:
            context["error"] = request.session.get("error")
            del request.session["error"]
        except:
            print("无error")
        return render(request, "qax2.html",context)

    select = request.POST.get("select")
    print(select)
    qa =qax2_emp()


    # {'content': '1399',
    #  'des': '仅剩1间/35.00㎡/1间在租/1室1厅1卫',
    #  'tag_list': ['新上', '独栋公寓', '月租', '有阳台', '开放厨房', '押一付一'],
    #  'title': '独栋·翔威公寓 飞跃科创园 主路旁边全新公寓 1室1厅'},
    data = qa.main()
    request.session["qax_data"] = data

    return redirect("/qax2")

@login_required(login_url='/login')
def reebuf(request):
    if request.method == "GET":
        context={}
        try:
            context["qax"] = request.session.get("reebuf_data")
            del request.session["reebuf_data"]
        except:
            print("reebuf_data错误吧")
        try:
            context["error"] = request.session.get("error")
            del request.session["error"]
        except:
            print("无error")
        return render(request, "reebuf.html",context)

    select = request.POST.get("select")
    print(select)
    if select == None or select=='':

        request.session["error"] = "输入不能为空"
        return redirect("/reebuf")
    qa =reebuf_emp()


    # {'content': '1399',
    #  'des': '仅剩1间/35.00㎡/1间在租/1室1厅1卫',
    #  'tag_list': ['新上', '独栋公寓', '月租', '有阳台', '开放厨房', '押一付一'],
    #  'title': '独栋·翔威公寓 飞跃科创园 主路旁边全新公寓 1室1厅'},
    data = qa.get_reebuf(select)
    request.session["reebuf_data"] = data

    return redirect("/reebuf")

@login_required(login_url='/login')
def user_mag(request):
    if request.method == "GET":
        context={}
        if request.user.is_superuser!=1 :
            context['error']='你的权限不足'
            return render(request, "user_management.html", context)
        user = User.objects.filter()
        l = []
        for u in user:
            item = {}
            item['username'] = u.username
            item['is_superuser'] = u.is_superuser
            item['email'] = u.email
            item['date_joined'] = '{0}/{1}/{2}'.format(u.date_joined.year,u.date_joined.month,u.date_joined.day)
            item['id']=u.id
            l.append(item)
        context['data']=l

        id = request.GET.get("id")
        button = request.GET.get("button")
        print(button,'id=',id)
        print(request.user)

        if button == 'del':
            user = User.objects.get(id=id)

            # 验证登录用户、待删除用户是否相同
            if request.user.is_superuser == 1:
                if request.user==user:
                    request.session["error"] = "不能删除自己"
                    return redirect("/user_mag")
                # 退出登录，删除数据并返回博客列表


                user.delete()

                request.session["error"] = "{0}删除成功".format(user.username)
                print("{0}删除成功".format(user.username))
                return redirect("/user_mag")
            else:

                request.session["error"] = "你没有删除操作的权限"
                return redirect("/user_mag")



        try:
            context["qax"] = request.session.get("reebuf_data")
            del request.session["reebuf_data"]
        except:
            print("reebuf_data错误吧")
        try:
            context["error"] = request.session.get("error")
            del request.session["error"]
        except:
            print("无error")
        return render(request, "user_management.html",context)

    if request.user.is_superuser != 1:
        context = {}
        context['error'] = '你的权限不足'
        return render(request, "user_management.html", context)

    POST = request.POST
    username=POST.get("username")
    id=POST.get("id")
    email=POST.get("email")
    password=POST.get("password")
    submit=POST.get("submit")
    if submit=='添加':
        if (password == None):
            request.session["error"] = '密码不能为空'
            return redirect("/user_mag")
        else:
            try:
                if email == '':
                    user_obj = User.objects.create_user(username=username, password=password)
                    print(user_obj)
                else:
                    user_obj = User.objects.create_superuser(username=username,password=password,email=email)
                    print(user_obj)
            except:
                request.session["error"] = '用户注册失败（用户名已存在）'
                return redirect("/user_mag")
        request.session["error"] = '注册成功！'
        return redirect("/user_mag")
    elif submit=='修改密码':
        user = User.objects.get(id=id)
        print(user)
        user.set_password(password)
        user.save()
        request.session["error"] = '密码修改成功'
        print('密码修改成功')
        return redirect("/user_mag")
    else:
        return redirect("/user_mag")








