from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from TestModel.models import Test


# 数据库操作
def testdb(request):
    l=Test.objects.all()
    print(l)

    return HttpResponse("<p>数据添加成功！</p>")