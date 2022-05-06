import json

from pprint import pprint
from threading import Lock, Thread

import requests

class reebuf_emp:
    def __init__(self):
        self.dic = []
        self.lock = Lock()
    def reebuf_emp(self,url):
        req = requests.get(url)

        rest = json.loads(req.text)

        data_list = rest['data']['list']
        print(url, '爬取中')

        for i in range(len(data_list)):
            data_i = data_list[i]
            self.lock.acquire()
            self.dic.append(data_i)
            self.lock.release()

    def get_reebuf(self,page):

        l=[]
        for ii in range(int(page)):
            url = 'https://www.freebuf.com/fapi/frontend/home/article?page={0}&limit=20&type=1&day=7&category=%E7%B2%BE%E9%80%89'.format(
                ii)



            t1 = Thread(target=self.reebuf_emp, args=(url,))
            l.append(t1)
            t1.start()
        for p in l:
            # 指定 thread 线程优先执行完毕
            p.join()
            # print(p)
            # self.get_item(urlss)


        return self.dic
if __name__ == '__main__':
    l=reebuf_emp()
    pprint(l.get_reebuf(5))