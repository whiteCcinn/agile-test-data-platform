import aiomysql

class MysqlPool:
    def __init__(self, host='127.0.0.1', port=3306,
                 user='root', password='',
                 db='mysql', loop=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.loop = loop

