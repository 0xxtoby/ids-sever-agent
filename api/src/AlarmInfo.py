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



if __name__ == '__main__':
    print(AlarmInfo_list().read_alarm_info(2))







