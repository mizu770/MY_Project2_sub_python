'''
Created on 2020. 11. 9

@author: USER
'''
from flask import Flask, render_template, request, jsonify, send_file, redirect
from webservice.Module import dbModule
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
from matplotlib import font_manager
import schedule
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
import matplotlib
import matplotlib.colors as mc
import colorsys
from random import randint
from matplotlib import font_manager, rc
import pymysql
import csv

#Flask 객체 생성

app = Flask(__name__)
@app.route("/chat",methods=["GET"])
def char_get(): 
    # 요청 방식이 GET 방식인지 POST 방식인지 다음과 같이 확인할 수 있다.
    print("methods : ", request.method)
    # get 방식 요청 파라미터를 읽어온다. 지정한 요청 파라미터가 없으면 None이 반환된다.
    id = request.args.get("id")
    pass1 = request.args.get("pass")
    uId = request.args.get("uId")
    # 템플릿 페이지(뷰 페이지)를 반환하면서 모델 정보를 인수로 지정할 수 있다.
    # 현재 모듈이 실행되는 위치에서 templates/chatting.html을 찾는다.
    # 뷰 페이지로 보낼 모델이 여러 개라면 아래와 같이 가변인수를 사용할 수 있다.
    return render_template("chatting.html", id = id, pass1 = pass1, uId = uId)

@app.route("/chat",methods=["POST"])
def char_post():
    # post 방식의 요청 파라미터를 읽어온다.
    print("methods : ", request.method)
    resData={}
    resData["id"] = request.form.get("id")
    resData["pass1"] = request.form.get("pass")
    resData["uId"] = request.form.get("uId")
    # 웹 서버 콘솔에 출력
    print("resData : ", resData)
    # 템플릿 페이지(뷰 페이지)를 반환하면서 모델 정보를 인수로 지정할 수 있다.
    # chat_get() 함수에서 사용했던 가변인수 방식과 동일하게 동작한다.
    # 템플릿으로 보내야 하는 모델 데이터가 많을 경우 유용하게 사용할 수 있다.
    # 뷰 페이지에서 resData 지정한 key 값으로 데이터에 접근할 수 있다.
    return render_template("chatting.html", **resData)

@app.route("/")
def home():
    method=request.args.get("method")
    print("home() - method", method)
    
    # get인지 post인지 확인
    
    print("method : ", request.method)

    DEVELOPER_KEY = "AIzaSyDFUg9YmkrscJEgep0t_FGsO-cWDX_PGqg"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    
    openFileName="id.json"
    fontLocation = "C:/Windows/fonts/malgun.ttf"
    fontName = font_manager.FontProperties(fname=fontLocation).get_name()
    with open("{}".format(openFileName), "r", encoding="utf-8") as openFile:
        readData = openFile.read()
        # 읽어 들인 파일의 데이터는 json 문자열이 배열 형식으로 되어 있기 때문에
        # loads() 함수를 사용해 json 문자열을 Python 자료구조인 사전으로
        # 디코딩 하여 리스트로 반환한다.
        jsonList = json.loads(readData)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    channelsId = []
    channelsTitle = []
    subscriberCount=[]
    channelImage1=[]
    channelImage=[]
    viewCount=[]
    for i in jsonList:
        search_response = youtube.channels().list(
        id=i["id"],
        part="statistics,snippet",
        fields ="items(id,statistics(subscriberCount,viewCount),snippet(title,thumbnails(medium(url))))",
        maxResults=1
        ).execute()
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            #if search_result["kind"] == "youtube#channel":
            channelsId.append("%s" % (search_result["id"]))
            subscriberCount.append("%s " % (search_result["statistics"]["subscriberCount"]))
            channelsTitle.append("%s" % (search_result["snippet"]["title"]))
            channelImage1.append("%s" %(search_result["snippet"]["thumbnails"]["medium"]["url"]))                             
            viewCount.append("%s" %(search_result["statistics"]["viewCount"]))
  
    subscriberCount = list(map(int, subscriberCount))
    viewCount = list(map(int, viewCount))
    for item in channelImage1:
        
        #문자열 치환
        item_mod = item.replace("", "")
    
        # 새로운 리스트에 추가
        channelImage.append(item_mod)
    try:
        db_class= dbModule.Database()
        for i in range(50) :
            sql = "INSERT INTO Trip (channelsId,channelsTitle,subscriberCount,viewCount,channelImage,times) VALUES ("+"'"+\
            channelsId[i]+"'"+','+"'"+channelsTitle[i]+"'"+','+str(subscriberCount[i])+','+str(viewCount[i])+","+"'"+channelImage[i]+"'"+",default)"
            db_class.execute(sql)
            db_class.commit()
        print("실행완료") 
        try :
            sql = "select channelsTitle, viewCount,date_format(times,'%Y-%m-%d') from Trip order by channelsTitle;"
            db_class.execute(sql)
            result = db_class.fetchall()
            result = pd.DataFrame(result)
            print("셀렉트 실행완료")
            result.columns=["name","value","date"]
      
            result["type"] = "유튜버"
            
            result=result[['name','value','type','date']]
            
            result.to_csv("D:\\SpringStudy4.7.1\\StarLuck\\src\\main\\webapp\\resources\\csv\\viewCount.csv",index=False)
            print("csv 파일 저장완료")
        finally:
            db_class.close()     
    finally:
            db_class.close()    
    return render_template("index.html",method=method)   
    #return render_template("index.html")       
schedule.every().day.at("18:19").do(home)             
# 현재 모듈이 최상위에 실행
if __name__ == "__main__":
    
    # 웹 서비스 시작
    
    app.run(host="0.0.0.0",port=9000,debug=True)
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except HttpError as e:
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))