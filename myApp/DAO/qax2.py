# -*-coding:utf-8 -*-

"""
# File       : teat.py
# Time       ：2021/10/28 18:58
# Author     ：toby
# version    ：python 3.6
# Description：
"""
import re
import requests
from bs4 import BeautifulSoup
from threading import Lock, Thread

class qax2_emp:

    def __init__(self):
        self.dic = []
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
            }
        self.lock = Lock()

    def get_item(self,url):
        req = requests.get(url, headers=self.headers).text

        html = BeautifulSoup(req, 'html.parser')
        print(url,'提取中')
        t = 0
        for i in html.findAll('section', class_="stream-list-item"):
            t += 1
            try:
                item = {}
                iv_data = i.find('div', class_="views hidden-xs").text
                iv = re.findall("\d+", iv_data)[0]
                url = i.find('h2', class_="title").find('a').attrs['href']
                title = i.find('h2', class_="title").find('a').text
                item['iv'] = iv
                item['title'] = title
                item['url'] = url

                self.lock.acquire()
                self.dic.append(item)
                self.lock.release()

            except:
                print("第{0}个元素提取错误".format(t))

    def main(self):
        l = []  # 线程列表
        for i in range(5):

            url_data = 'https://forum.butian.net/questions?page='
            urlss = url_data + str(i)

            t1 = Thread(target=self.get_item,args=(urlss,))
            l.append(t1)
            t1.start()


        for p in l:
            # 指定 thread 线程优先执行完毕
            p.join()
            # print(p)
            # self.get_item(urlss)

        return self.dic


if __name__ == '__main__':
    a=qax_2()
    print(a.main())
