import time
from pprint import pprint

from api.src.db_util import DBUtil


class AlertInfo:
    def __init__(self):
        self.alrm_id= 0
        self.alrm_type = ''#警告类型
        self.alrm_desc = ''#告警描述
        self.alrm_time = ''#警告发生时间

        self.alrm_rule = ''#匹配规则
        self.alrm_rule_name = ''#匹配规则名称

        self.src_ip = ''#源IP
        self.src_port = ''#源端口
        self.dst_ip = ''#目的IP
        self.dst_port = ''#目的端口
        self.proto_data = ''#协议数据




    #创建sqlit数据表
    def create_table(self):
        db=DBUtil().db
        sql = """
        create table if not exists alert_info(
        alrm_id integer primary key autoincrement,
        alrm_type text,
        alrm_desc text,
        alrm_time text,
        alrm_rule text,
        alrm_rule_name text,
        src_ip text,
        src_port text,
        dst_ip text,
        dst_port text,
        proto_data text
        )
        """
        db.execute(sql)
        db.commit()
        db.close()


    # 保存警告信息
    def save_aler(self):
        sql = """
        insert into alert_info(alrm_type,alrm_desc,alrm_time,alrm_rule,src_ip,src_port,dst_ip,dst_port,proto_data,alrm_rule_name)
        values(?,?,?,?,?,?,?,?,?,?)
        """
        self.db.execute(sql,(self.alrm_type,self.alrm_desc,self.alrm_time,self.alrm_rule,self.src_ip,self.src_port,self.dst_ip,self.dst_port,self.proto_data,self.alrm_rule_name))
        self.db.commit()
        self.db.close()

class AlarmInfo_list:
    def __init__(self):
        self.alarmInfo_list = []



    #读取一页数据
    def read_alarm_info(self,page_num=1,page_size=20):
        db=DBUtil().db
        page_num=(page_num-1)*page_size+1
        sql = """
        select * from alert_info limit ?,?
        """
        cuoer = db.execute(sql,(page_num,page_size))
        for row in cuoer:
            alarmInfo = AlertInfo()
            alarmInfo.alrm_id = row[0]
            alarmInfo.alrm_type = row[1]
            alarmInfo.alrm_desc = row[2]
            alarmInfo.alrm_time = row[3]
            #字符串时间戳输出
            alarmInfo.alrm_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(alarmInfo.alrm_time)))
            alarmInfo.alrm_rule = row[4]
            alarmInfo.alrm_rule_name = row[5]
            alarmInfo.src_ip = row[6]
            alarmInfo.src_port = row[7]
            alarmInfo.dst_ip = row[8]
            alarmInfo.dst_port = row[9]
            alarmInfo.proto_data = row[10]
            self.alarmInfo_list.append(alarmInfo)
        db.close()
        r_data_list = []
        for i in self.alarmInfo_list:
            r_data_list.append([i.alrm_id,i.alrm_type,i.alrm_desc,i.alrm_time,i.alrm_rule,i.alrm_rule_name,i.src_ip,i.src_port,i.dst_ip,i.dst_port,i.proto_data])
        return r_data_list

    def select_id(self,alrm_id):
        db=DBUtil().db
        sql = """
        select * from alert_info where alrm_id=?
        """
        cuoer = db.execute(sql,(alrm_id,))
        for row in cuoer:
            alarmInfo = AlertInfo()
            alarmInfo.alrm_id = row[0]
            alarmInfo.alrm_type = row[1]
            alarmInfo.alrm_desc = row[2]
            alarmInfo.alrm_time = row[3]
            #字符串时间戳输出
            alarmInfo.alrm_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(alarmInfo.alrm_time)))
            alarmInfo.alrm_rule = row[4]
            alarmInfo.alrm_rule_name = row[5]
            alarmInfo.src_ip = row[6]
            alarmInfo.src_port = row[7]
            alarmInfo.dst_ip = row[8]
            alarmInfo.dst_port = row[9]
            alarmInfo.proto_data = row[10]
            db.close()
            return [alarmInfo.alrm_id,alarmInfo.alrm_type,alarmInfo.alrm_desc,alarmInfo.alrm_time,alarmInfo.alrm_rule,alarmInfo.alrm_rule_name,alarmInfo.src_ip,alarmInfo.src_port,alarmInfo.dst_ip,alarmInfo.dst_port,alarmInfo.proto_data]




    #读取有几页
    def get_page_num(self,page_size=20):
        db=DBUtil().db
        sql = """
        select count(*) from alert_info
        """
        cuoer = db.execute(sql)
        for row in cuoer:
            page_num = row[0]//page_size
            if row[0]%page_size!=0:
                page_num+=1
        db.close()
        return page_num

    #查询alrm_type字段数据
    def select_alrm_type(self):
        db=DBUtil().db
        sql = """
        select distinct alrm_type from alert_info
        """
        cuoer = db.execute(sql)
        alrm_type_list = []
        for row in cuoer:
            alrm_type_list.append(row[0])
        db.close()
        return alrm_type_list

    #查询遍历不同alrm_type 的数据条数
    def get_alrm_type_num(self):
        db=DBUtil().db
        types=self.select_alrm_type()
        num_list = []
        for type in types:
            sql = """
            select count(*) from alert_info where alrm_type=?
            """
            cuoer = db.execute(sql,(type,))
            for row in cuoer:
                num_list.append([type,row[0]])

        db.close()
        return num_list

    def select_rule_name(self):
        db=DBUtil().db
        sql = """
        select distinct alrm_rule_name from alert_info
        """
        cuoer = db.execute(sql)
        rule_name_list = []
        for row in cuoer:
            rule_name_list.append(row[0])
        db.close()
        return rule_name_list

    def get_rule_name_num(self):
        db=DBUtil().db
        types=self.select_rule_name()
        num_list = []
        for type in types:
            sql = """
            select count(*) from alert_info where alrm_rule_name=?
            """
            cuoer = db.execute(sql,(type,))
            for row in cuoer:
                num_list.append([type,row[0]])

        db.close()
        return num_list

    def read_alarm_info_by_ip_rule_type(self,ip,rule_name,alrm_type,page_num=1,page_size=20):
        db=DBUtil().db

        sql = """
        select count(*)  from alert_info where (src_ip=? or ? is '') and (alrm_rule_name=? or ? is '' )and (alrm_type=? or ?is '' )
        """
        cuoer = db.execute(sql,(ip,ip,rule_name,rule_name,alrm_type,alrm_type))
        for row in cuoer:
            sum=row[0]
        sum=sum//page_size+1



        sql = """
        select * from alert_info where (src_ip=? or ? is '') and (alrm_rule_name=? or ? is '' )and (alrm_type=? or ?is '' )limit ?,?
        """
        cuoer = db.execute(sql,(ip,ip,rule_name,rule_name,alrm_type,alrm_type,(page_size*(page_num-1)),page_size))
        alarm_info_list = []
        for row in cuoer:
            alarmInfo = AlertInfo()
            alarmInfo.alrm_id = row[0]
            alarmInfo.alrm_type = row[1]
            alarmInfo.alrm_desc = row[2]
            alarmInfo.alrm_time = row[3]
            # 字符串时间戳输出
            alarmInfo.alrm_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(alarmInfo.alrm_time)))
            alarmInfo.alrm_rule = row[4]
            alarmInfo.alrm_rule_name = row[5]
            alarmInfo.src_ip = row[6]
            alarmInfo.src_port = row[7]
            alarmInfo.dst_ip = row[8]
            alarmInfo.dst_port = row[9]
            alarmInfo.proto_data = row[10]
            self.alarmInfo_list.append(alarmInfo)
        db.close()
        r_data_list = []
        for i in self.alarmInfo_list:
            r_data_list.append(
                [i.alrm_id, i.alrm_type, i.alrm_desc, i.alrm_time, i.alrm_rule, i.alrm_rule_name, i.src_ip, i.src_port,
                 i.dst_ip, i.dst_port, i.proto_data])
        return r_data_list,sum

    def read_rule_name(self):
        db=DBUtil().db
        sql = """
        select distinct alrm_rule_name from alert_info
        """
        cuoer = db.execute(sql)
        rule_name_list = []
        for row in cuoer:
            rule_name_list.append(row[0])
        db.close()
        return rule_name_list
    def read_rule_type(self):
        db=DBUtil().db
        sql = """
        select distinct alrm_type from alert_info
        """
        cuoer = db.execute(sql)
        rule_type_list = []
        for row in cuoer:
            rule_type_list.append(row[0])
        db.close()
        return rule_type_list
    def read_ip(self):
        db=DBUtil().db
        sql = """
        select distinct src_ip from alert_info
        """
        cuoer = db.execute(sql)
        ip_list = []
        for row in cuoer:
            ip_list.append(row[0])
        db.close()
        return ip_list










if __name__ == '__main__':
    # print(AlarmInfo_list().get_alrm_type_num(),AlarmInfo_list().get_rule_name_num())
    print(AlarmInfo_list().read_alarm_info_by_ip_rule_type('','','',1,20))
    print(AlarmInfo_list().read_alarm_info(1))
    print(AlarmInfo_list().read_rule_name(),AlarmInfo_list().read_rule_type(),AlarmInfo_list().read_ip())







