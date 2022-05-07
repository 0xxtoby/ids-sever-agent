import datetime
import time
from queue import Queue

import toml

from api.src.AlarmInfo import AlertInfo


class Authlog():
    def __init__(self):
        self.time = ""
        self.ip = ""
        self.stutus = ""
        self.msg = ""
        self.src = ""
        self.port = ""
        self.user = ""

    def get_dict(self):
        return {
            "time": self.time,
            "ip": self.ip,
            "status": self.status,
            "msg": self.msg,
            "src": self.src,
            "port": self.port,
            "user": self.user
        }

    #log 解析
    def parse_log(self, line='May  5 19:13:01 localhost CRON[6637]: pam_unix(cron:session): session closed for user root'):

        try:
            LL=line
            L=line.split(': ')
            line = L[0].split(' ')
            t=LL[:14]

            self.time = datetime.datetime.strptime(t, '%b %d %H:%M:%S')
            self.ip = line[4]
            self.status = line[4]
            for i in L[1:]:
                self.msg +=i
        except Exception as e:
            print('excp:',e,LL)





class AuthLogs:
    def __init__(self, log_data):
        self.cfg = toml.load('./api/ids.toml')
        self.log_data = log_data
        self.log_list = []

        for line in self.log_data.split('\n'):
            log = Authlog()
            log.parse_log(line)
            self.log_list.append(log)

    def get_log_list(self):
        return self.log_list

    def alert(self, alert_info,alert_list):
        with open(self.cfg['agent_log'], 'a', encoding='utf-8') as f:
            f.write(alert_info)
            f.write('\n')
        #     [E[-1].src,E[-1].port, log.time, sun,E[-1].msg]]
        Alert=AlertInfo()
        Alert.src_ip=alert_list[0]
        Alert.src_port=alert_list[1]
        Alert.alrm_time=time.mktime(alert_list[2].replace(year=datetime.datetime.now().year).timetuple())
        Alert.alrm_rule="间隔30秒内同一个IP连续{}次失败".format(alert_list[3])
        Alert.alrm_rule_name="ssh爆破"
        Alert.proto_data=alert_list[4]
        Alert.alrm_type="系统日志审计"
        Alert.save_aler()





    #ssh爆破识别
    def ssh_brute(self):
        sun=0
        E=[]
        for log in self.log_list:
            msg=log.msg
            if  'Failed password' in msg[:len("Failed password for")]:
                    for i in range(len(msg.split(' '))) :
                        if msg.split(' ')[i] == 'from':

                            log.src = msg.split(' ')[i + 1]
                            log.port = msg.split(' ')[i + 3]


                            if E != []:
                                # print((log.time - E[-1].time).total_seconds())
                                if (log.time - E[-1].time).total_seconds() < 30:
                                    sun += 1
                                else:
                                    if sun!=0 and sun >=5:
                                        # | xss跨站脚本攻击 | [+]检测到威胁 10.74.41.52->176.28.50.165 /hpp/params.php?pp=12&p=valid1%3Cscript%3Ealert(42873)%3C/script%3E
                                        info = "|ssh爆破| [+]检测到威胁 {} -> {}连续尝试登录 {} 次  ".format(E[-1].src,
                                                                                            log.time.__format__(
                                                                                                "%m-%d %H:%M:%S"), sun)

                                        info_list= [E[-1].src,E[-1].port, log.time, sun,E[-1].msg]
                                        self.alert(info,info_list)
                                        print(info)
                                    sun = 0
                                    E = []
                            E.append(log)

                    #格式化输出log.time
                    t = log.time.__format__("%m-%d %H:%M:%S")
                    info="[*] {} 检测到ssh连接失败: {}:{}".format(t,log.src, log.port)

                    print(info)


    #读取规则
    def get_rules(self):
        pass


if __name__ == '__main__':




    a=Authlog()
    a.parse_log()

    with open('api/data/auth.log', 'rb') as f:
        log_data = f.read()
        AuthLogs = AuthLogs(log_data.decode("utf-8"))
        AuthLogs.ssh_brute()