import re
import socket, sys
from pprint import pprint

from threading import Thread, Lock

socket.setdefaulttimeout(2)
ip =input("请输入ip：") # 接收参数
ports =input("请输入端口范围(例： 1-65535)：") # 接收参数

#判断端口是否开放
def port_scan(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()

def get_ip_port(ip, start_port, end_port):
    def if_port(ip,port):
        if port_scan(ip, port):
            lock.acquire()
            print('[+]' + ip + ':' + str(port) + ' Open')
            a.append(port)
            lock.release()
        else:
            # print('[-]' + ip + ':' + str(port) + ' Close')
            pass

    a=[]  # 结果列表

    lock = Lock() #线程锁
    l = []  # 线程列表
    for port in range(int(start_port), int(end_port) + 1):
        t1 = Thread(target=if_port, args=(ip, port))
        l.append(t1)
        t1.start()
    # 等待所有线程执行完毕
    for p in l:
        # 指定 thread 线程优先执行完毕
        p.join()
        # print(p)
    return a #返回打开端口列表


def xieyifenxi(i,t):
    ip_port = (ip, i)
    print(str(t) + '/' + str(len(a)) + '  ' + "port=" + str(i))
    # print(ip_port)

    s = socket.socket()  # 创建套接字
    try:
        s.connect(ip_port)  # 连接服务器
        s.sendall('123213\n'.encode())
        server_reply = s.recv(1024)
        item = {}
        item["port"] = str(i)
        #判断端口类型
        if re.search("FTP", str(server_reply)) != None:
            item["type"] = 'FTP'
        elif re.search("SSH", str(server_reply)) != None:
            item["type"] = 'SSH'
        elif b'\xff\xfb' in server_reply:
            item["type"] = 'telnet'
        elif re.search("smtp", str(server_reply)) != None:
            item["type"] = 'smtp'
        elif re.search("HTTP", str(server_reply)) != None:
            item["type"] = 'HTTP'
        elif re.search("OK Dovecot ready", str(server_reply)) != None:
            item["type"] = 'pop3'
        elif re.search("IMAP", str(server_reply)) != None:
            item["type"] = 'IMAP'
        elif b'I\x00\x00\x00' in server_reply:
            item["type"] = 'mysql'
        elif re.search("ERR", str(server_reply)) != None:
            item["type"] = 'rdp'
        elif re.search("RFB", str(server_reply)) != None:
            item["type"] = 'vnc'
        elif re.search("ERROR\r\n", str(server_reply)) != None:
            item["type"] = 'memcache'
        else:
            item["type"] = '无法识别'
            s.close()
            return
        #临界资源保护
        lock.acquire()
        dic.append(item)
        lock.release()
        #关闭连接
        s.close()
    except Exception as e:
        pass

if __name__ == '__main__':
    #扫描已打开的端口
    if '-' in ports:
        ports = ports.split('-')
        a=get_ip_port(ip, ports[0], ports[1])
    else:
        print('输入错误')

    # 端口协议分析
    dic=[]#结果列表

    lock = Lock()
    l = []#线程列表
    t=0
    for i in a:
        t+=1
        t1 = Thread(target=xieyifenxi, args=(i, t))
        l.append(t1)
        t1.start()
    # 等待所有线程执行完毕
    for p in l:
        # 指定 thread 线程优先执行完毕
        p.join()
        # print(p)
    print("\n识别成功的端口有：")
    pprint(dic)