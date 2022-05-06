from pprint import pprint

from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User

user = User.objects.filter(id="16")
l=[]
for u in user:
    item={}
    item['username']=u.username
    item['is_superuser']=u.is_superuser
    item['email']=u.email
    item['date_joined']=u.date_joined
    item['id']=u.id
    l.append(item)
pprint(l)
