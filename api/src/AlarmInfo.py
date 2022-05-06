from api.src.db_util import DBUtil


class AlertInfo:
    def __init__(self):
        self.db = DBUtil().db

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
        self.db.execute(sql)
        self.db.commit()
        self.db.close()


    # 保存警告信息
    def save_aler(self):
        sql = """
        insert into alert_info(alrm_type,alrm_desc,alrm_time,alrm_rule,src_ip,src_port,dst_ip,dst_port,proto_data,alrm_rule_name)
        values(?,?,?,?,?,?,?,?,?,?)
        """
        self.db.execute(sql,(self.alrm_type,self.alrm_desc,self.alrm_time,self.alrm_rule,self.src_ip,self.src_port,self.dst_ip,self.dst_port,self.proto_data,self.alrm_rule_name))
        self.db.commit()
        self.db.close()







