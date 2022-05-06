# -*-coding:utf-8 -*-

"""
# File       : test.py
# Time       ：2021/11/7 12:15
# Author     ：toby
# version    ：python 3.6
# Description：
"""
from threading import Thread,Lock
import requests
import xlwt
from lxml import etree

class qax_emp:
    def __init__(self):
        pass

    def write_file(self,item):
        book = xlwt.Workbook(encoding='utf-8')
        sheet1 = book.add_sheet("sheet", cell_overwrite_ok=True)

        sheet1.col(0).width = 256 * 59
        sheet1.col(1).width = 256 * 68

        sheet1.write(0, 0, "标题")
        sheet1.write(0, 1, "链接")

        for i in range(len(item)):
            sheet1.write(i + 1, 0, item[i]["title"])
            sheet1.write(i + 1, 1, item[i]["href"])

        book.save("漏洞.xls")

    def get_item(self,search):
        url = 'https://forum.butian.net/search/community?word=%E6%BC%8F%E6%B4%9E'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
        }
        item = []
        req = requests.get(url, headers=headers)
        html = etree.HTML(req.text)
        pg_max = html.xpath('/html/body/div[3]/div/div/div[2]/div[1]/div/ul/li/a')[-2].text
        print('共' + pg_max + '页')

        # search='漏洞'
        def sdsd(search, pg):
            url = "https://forum.butian.net/search/community?word={0}&page={1}".format(search, pg + 1)
            req = requests.get(url, headers=headers)
            print("正在爬取第" + str(pg + 1) + '页')
            html = etree.HTML(req.text)
            i_len = len(html.xpath("/html/body/div[3]/div/div/div[2]/div[1]/section"))
            for i in range(i_len):
                data = {}
                title = html.xpath("/html/body/div[3]/div/div/div[2]/div[1]/section[{0}]/h2/a//text()".format(i + 1))
                href = html.xpath("/html/body/div[3]/div/div/div[2]/div[1]/section[{0}]/h2/a/@href".format(i + 1))

                title_data = ''
                for t in title:
                    title_data += t
                data['title'] = title_data
                data['href'] = href

                lock.acquire()
                item.append(data)
                lock.release()
        l = []  # 线程列表
        lock=Lock()
        for pg in range(int(pg_max)):
            t1 = Thread(target=sdsd, args=(search, pg))
            l.append(t1)
            t1.start()
            # print(item)

        for p in l:
            # 指定 thread 线程优先执行完毕
            p.join()
            # print(p)

        return item
        # print(i_len,title,href)
        # print(req.text)

if __name__ == '__main__':
    q=qax_emp()
    a=q.get_item("漏洞")
    print(a)