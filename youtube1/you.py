'''
Created on 2020. 10. 27

@author: USER
'''

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pymysql
import json
from matplotlib import font_manager
import schedule
import time
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
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

def youtube_channels():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  #mysql 접속
  Trip = pymysql.connect(
        user="root",
        passwd="12345678",
        host="127.0.0.1",
        db="spring",
        charset='utf8mb4'
        )
  channelsId = []
  channelsTitle = []
  subscriberCount=[]
  channelImage1=[]
  channelImage=[]
  viewCount=[]
  
  # Call the search.list method to retrieve results matching the specified
  # query term.
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
        cursor = Trip.cursor()
        for i in range(50) :
            sql = "INSERT INTO Trip (channelsId,channelsTitle,subscriberCount,viewCount,channelImage,times) VALUES ("+"'"+\
            channelsId[i]+"'"+','+"'"+channelsTitle[i]+"'"+','+str(subscriberCount[i])+','+str(viewCount[i])+","+"'"+channelImage[i]+"'"+",default)"
            cursor.execute(sql)
        Trip.commit()
        print("실행완료")    
  finally:
            Trip.close()

schedule.every().day.at("09:30").do(youtube_channels)

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
   while True:
    schedule.run_pending()
    time.sleep(1)
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))