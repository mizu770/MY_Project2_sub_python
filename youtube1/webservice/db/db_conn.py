'''
Created on 2020. 11. 10

@author: USER
'''
import pymysql

def create():
   
    try:
        db = pymysql.connect(user="root",
        passwd="12345678",
        host="127.0.0.1",
        db="pythondb",
        charset='utf8'
        )
        with db.cursor() as cursor:     
            sql ="""
                    CREATE TABLE IF NOT EXISTS Trip(    
                    channelsId varchar(150),
                    channelsTitle varchar(100),
                    subscriberCount int(11),
                    viewCount int(11),
                    channelImage text(200),
                    times timestamp Default now()
                )ENGINE=InnoDB DEFAULT CHARSET=utf8;
                    """     
            cursor.execute(sql)
            
            db.commit()
    finally:
        db.close()
        
def insert():   
    
    id=["midas","admin","servlet"]
    name=["홍길동","이순신","강감찬"]
    pw=["1234","1234","1234"]
    email=["midastop@naver.com","midastop1@naver.com","midas@daum.net"]
    phone=["010-1234-5678","010-4321-8765","010-5687-5678"]
    address1=["경기 부천시 오정구 수주로 18 (고강동, 동문미도아파트)","서울 구로구 구로중앙로34길 33-4(구로동, 영림빌딩)","서울 강남구 강남대로146길 28 (논현동, 논현아파트)"]
    reg_date=["2019-10-06 12:10:30","2019-10-11 11:20:50","2019-10-05 12:10:30"]
    
    try :
        db = pymysql.connect(user="root",
        passwd="12345678",
        host="127.0.0.1",
        db="pythondb",
        charset='utf8'
        )
        with db.cursor() as cursor:
            for i in range(3):   
                sql1 = "INSERT INTO member(id, name, pass, email, phone, address1, reg_date) VALUES("+"'"+id[i]+"'"+","+"'"+name[i]+"'"+","+"'"+pw[i]+"'"+","+"'"+email[i]+"'"+","+"'"+phone[i]+"'"+","+"'"+address1[i]+"'"+","+"'"+reg_date[i]+"'"+");"
                cursor.execute(sql1)
        db.commit()
    finally:
        db.close()
def select():
    db = pymysql.connect(user="root",
        passwd="12345678",
        host="127.0.0.1",
        db="pythondb",
        charset='utf8'
        )
    try:
        with db.cursor() as cursor:
            sql = 'SELECT * FROM member WHERE email = %s'
            cursor.execute(sql, ('test@test.com',))
            result = cursor.fetchone()
        print(result)
        # (1, 'test@test.com', 'my-passwd')
    finally:
            db.close()