from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

## html 을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## api 역할
@app.route('/memo', methods=['POST'])
def post_articles():
    # 1. 클라이언트로부터 데이터를 받기
    url_recieve = request.form['url_give']
    comment_recieve = request.form['comment_give']
    
    # 2. meta tag 를 스크래핑하기
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    
    data = requests.get(url_recieve, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.

    og_title = soup.select_one('meta[property="og:title"]')
    og_image = soup.select_one('meta[property="og:image"]')
    og_description = soup.select_one('meta[property="og:description"]')

    # print(og_title)
    # print(og_image)
    # print(og_description)

    url_title = og_title['content']
    url_image = og_image['content']
    url_description = og_description['content']


    article = {'url': url_recieve, 'title':url_title, 'desc':url_description,
               'img':url_image, 'comment':comment_recieve}
    
    # 3. mongoDB에 데이터 넣기
    db.articles.insert_one(article)
    
    return jsonify({'result':'success'})

@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. 모든 도큐먼트 찾기, _oid 값은  출력에서 제외하기
    result = list(db.articles.find({}, {'id':0}))
    # 2. articles 라는 키 값으로 article 정보 내려주기
    return jsonify({'result':'success', 'articles':result})  # 헴은바보///....



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)