import toml
import  sqlite3

#db_util类
class DBUtil:
    #初始化
    def __init__(self):
        self.db = sqlite3.connect('db.sqlite3')
        self.cursor = self.db.cursor()
    def close(self):
        self.db.close()

