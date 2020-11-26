'''
Created on 2020. 11. 10

@author: USER
'''
import pymysql
 
class Database():
    def __init__(self):
        self.db = pymysql.connect(user="root",
                                    passwd="12345678",
                                    host="127.0.0.1",
                                    db="pythondb",
                                    charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args)  
        row = self.cursor.fetchone()
        return row
    
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()
