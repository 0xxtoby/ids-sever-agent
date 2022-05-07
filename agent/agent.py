import json
import os
import time

import requests
import toml



cfg = toml.load('./agent/config.toml')

class data_dic:
    def __init__(self):
        self.name = cfg['agent']['name']
        self.ip = cfg['server']['ip']
        self.port = cfg['server']['port']
        self.data = ''
        self.type = ''
        self.id = ''
        self.system = '1'
        self.datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def get_dict(self):
        data_dic = {
            'name': self.name,
            'ip': self.ip,
            'port': self.port,
            'data': self.data,
            'type': self.type,
            'id': self.id,
            'system': self.system,
            'datetime': self.datetime,

        }
        return data_dic

    # 信息发送
    def send_data(self, ff):
        url = "http://{}:{}/api/agent_msg/".format(cfg['server']['ip'], cfg['server']['port'])
        r = requests.post(url, self.get_dict(), files={'file': ff})
        print(r.text)
        return r.text
class agent:

    def __init__(self):
        self.name = ''
        self.ip = ''
        self.port = ''
        self.data = ''
        self.type = ''

    #log扫描
    def web_log_scan(self):

        item=data_dic()
        item.type='1'
        files=cfg['log']['los_files']
        for i in files:
            with open(i, "rb") as f:
             ff=f.read()
             item.send_data(ff)





    #系统日志扫描
    def system_log_scan(self):
        time = data_dic()
        time.type = '4'

        for file in cfg['log']['system_log_files']:

            with open(file, "rb") as f:
                ff = f.read()
                time.send_data(ff)


    #pacp扫描
    def pacp_scan(self):
        time = data_dic()
        time.type='3'

        for path in cfg['log']['pcap_dirs']:
            for root, dirs, files in os.walk(path):
                for file in files:
                        with open(os.path.join(root, file), "rb") as f:
                            ff = f.read()
                            time.send_data(ff)



    def run(self):
        self.pacp_scan()
        self.system_log_scan()
        self.web_log_scan()




def send_data(data, ff):
        url = "http://{}:{}/api/agent_msg/".format(cfg['server']['ip'], cfg['server']['port'])
        r = requests.post(url, data, files={'file': ff})
        print(r.text)

if __name__ == '__main__':
    agent().run()



