from django.shortcuts import render

def runoob(request):
  views_name = "θιΈζη¨"
  return  render(request,"runoob.html", {"name":views_name})