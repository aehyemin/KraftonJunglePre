import re
import random
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.


db.memos.insert_one({'title':'첫번째 제목을 입력합니다', 'content':'첫번째 내용을 입력합니다','likes':0})
db.memos.insert_one({'title':'두번째 제목을 입력합니다', 'content':'두번째 내용을 입력합니다','likes':1})

all = list(db.memos.find({}))
print(all)