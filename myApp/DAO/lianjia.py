from pprint import pprint
from threading import Lock, Thread

from lxml import etree

import xlwt
import requests



class lianjia_emp:
    def __init__(self):
        self.item = []
        self.lock=Lock()

    def get_dis(self,url, headers, cooke):
        req = requests.get(url=url, headers=headers)
        html = etree.HTML(req.text)

        d_len = len(html.xpath('//*[@id="content"]/div[1]/div[1]/div/div/p[1]/a/text()'))
        for i in range(d_len):
            i += 1
            data_dis = {}
            title_list = html.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/div/p[1]/a/text()'.format(i))  # 标题
            content_list = html.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/div/span/em/text()'.format(i))  # 价格
            des_a_list = html.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/div/p[2]/a/text()'.format(i))  # des
            des_i_list = html.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/div/p[2]/text()'.format(i))  # des
            tag_list = html.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/div/p[3]/i/text()'.format(i))  # 特色

            # print(title_list[0].strip())
            # print(content_list[0])
            # print(des_a_list[0]+'-'+des_a_list[1]+'-'+des_a_list[2]+'/'+des_i_list[4].strip()+'/'+des_i_list[5].strip()+'/'+des_i_list[6].strip())
            # print(tag_list)

            data_dis['title'] = title_list[0].strip()
            data_dis['content'] = content_list[0]
            try:
                data_dis['des'] = des_a_list[0] + '-' + des_a_list[1] + '-' + des_a_list[2] + '/' + des_i_list[
                    4].strip() + '/' + \
                                  des_i_list[5].strip() + '/' + des_i_list[6].strip()
            except:
                try:
                    des_a_list = html.xpath('//*[@id="content"]/div[1]/div[1]/div[{0}]/div/p[2]/*/text()'.format(i))
                    data_dis['des'] = des_a_list[0] + '/' + des_i_list[
                        2].strip() + '/' + \
                                      des_i_list[3].strip() + '/' + des_i_list[4].strip()
                except:
                    print('des错误')

            data_dis['tag_list'] = tag_list
            # print(data_dis)
            self.lock.acquire()
            self.item.append(data_dis)
            self.lock.release()

    def main(self,dp_no,fs_no,zj_no,hx_no,cx_no,pg):
        url = 'https://taizhou.lianjia.com/zufang/'
        cookie_data = '''
            lianjia_uuid=0359d84e-2e4f-43df-9819-c9cdda64546c; lianjia_ssid=7b3820dc-6662-4b55-a072-00d1aaf7747a; _smt_uid=617f8ec5.f6ce3b4; UM_distinctid=17cda45b4a28c8-0413928f6640fd-1c306851-1fa400-17cda45b4a37e9; _jzqa=1.292944431187657000.1635749574.1635749574.1635749574.1; _jzqc=1; _jzqx=1.1635749574.1635749574.1.jzqsr=cn.bing.com|jzqct=/.-; _jzqckmp=1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross={"distinct_id":"17cda45b66083a-00eea5c552fca9-1c306851-2073600-17cda45b661c02","$device_id":"17cda45b66083a-00eea5c552fca9-1c306851-2073600-17cda45b661c02","props":{"$latest_traffic_source_type":"自然搜索流量","$latest_referrer":"https://cn.bing.com/","$latest_referrer_host":"cn.bing.com","$latest_search_keyword":"未取到值"}}; _ga=GA1.2.205791987.1635749576; _gid=GA1.2.407283806.1635749576; login_ucid=2000000223671382; lianjia_token=2.0012631eb27794870803ce37835539e48e; lianjia_token_secure=2.0012631eb27794870803ce37835539e48e; security_ticket=mFHDgjD7fauVVI9LdDcVBsMw3YzwzGNBIrGUPFG9QfpMZ9lvmFUgCvJJHOWkcH9ODGKZGd0K0jviq7nKZm9ck7wMlpmLglU7pRqIfvOKz8FAvUpDLh9HcaCKPf6Zv8WVuwO4Byz8n7JXDGtkWirS2eYQpKYEe46SWgP5kTLNQWQ=; select_city=331000; _qzja=1.1862298442.1635749651612.1635749651612.1635749651612.1635749651612.1635749651612.0.0.0.1.1; _qzjc=1; _qzjto=1.1.0; _jzqb=1.5.10.1635749574.1; CNZZDATA1254525948=49301376-1635739350-https%3A%2F%2Fwww.lianjia.com%2F|1635739350; CNZZDATA1255633284=1477882295-1635742587-https%3A%2F%2Fwww.lianjia.com%2F|1635742587; CNZZDATA1255604082=93221754-1635740769-https%3A%2F%2Fwww.lianjia.com%2F|1635740769; _qzjb=1.1635749651612.1.0.0.0; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMjllN2QzYzY2NDE5YjY4MzYyYzczMjM4YTE0ODAzZDY0Mzk2Yzc2MWM3ZWJmZWMwNDY4NDVkMWMwNGJhMmI4NzZiODkzMmM5Y2E4M2Q2NTJjZmE1Y2QyZDdiYWM3NmYxMTExY2YxM2VkMmM1ZTZhZjlkYWQxYTFhYTljNWQ5MDIyNzUzMTYyMzY2ZjhlYzdkZjdiZmU4ODZlYTk2MzhiOGMzMDE5NjQxZmI4ZmQwMGUwZjhhOTg0YzAwZTNmMmRlYmI5YTZjZTY0NmNjMWQ0ZGUyMWVmZjI4NTRmNzM3YzQzYTBmODNjZTJmOTU1MGU0OTY0OTA3OTE2N2YxOWMxN2Y3MjA0OGU1ZGY0MjY1NGJhZWM4NDViZmNjMmEzOWVmNjBhZjg5M2QwOTY5NjUxM2VlMjIyM2UzNmIxZWE2ZTBhZDJjYTgwYWIwY2RmODkxNzM3NGY2ZTYwNTUxMzUzNFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI0ODg2NmI1M1wifSIsInIiOiJodHRwczovL3RhaXpob3UubGlhbmppYS5jb20venVmYW5nLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0',
        }

        cookieDict = {}
        cookies = cookie_data.split("; ")
        for co in cookies:
            co = co.strip()
            p = co.split('=')
            value = co.replace(p[0] + '=', '').replace('"', '')
            cookieDict[p[0]] = value

        # print(cookieDict)
        dp_list = ['', 'sanmenxian', 'linhaishi', 'xianjuxian', 'tiantaixian', 'jiaojiangqu', 'wenlingshi', 'yuhuanshi',
                   'luqiaoqu', 'huangyanqu']
        fs_list = ['', 'rt200600000001', 'rt200600000002']
        zj_list = ['', 'rp1', 'rp2', 'rp3', 'rp4', 'rp5', 'rp6', 'rp7']
        cx_list = ['', 'f100500000001', 'f100500000005', 'f100500000003', 'f100500000007', 'f100500000009']
        hx_list = ['', 'l0', 'l1', 'l2', 'l3']

        dp = dp_list[int(dp_no)]
        fs = fs_list[int(fs_no)]
        zj = zj_list[int(zj_no)]
        hx = hx_list[int(hx_no)]
        cx = cx_list[int(cx_no)]

        pg = int(pg)





        l = []  # 线程列表

        for i in range(pg):
            p = 'pg' + str(i + 1)
            url_data = 'https://taizhou.lianjia.com/zufang/{0}/{5}{1}{3}{2}{4}/'.format(dp, fs, zj, hx, cx, p)
            print(url_data)
            print("正在抓取第{0}页...".format(i + 1))
            # self.get_dis(url_data, headers, cookieDict)
            t1 = Thread(target=self.get_dis, args=(url_data, headers, cookieDict))
            l.append(t1)
            t1.start()
            # print(item)

        for p in l:
            # 指定 thread 线程优先执行完毕
            p.join()
            # print(p)

        return self.item
if __name__ == '__main__':
    a=lianjia_emp()
    print(a.main(0,0,0,0,0,5))






