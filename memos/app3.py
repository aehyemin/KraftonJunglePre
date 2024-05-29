from bson import ObjectId
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys

app = Flask(__name__)

client = MongoClient('localhost',27017)
# client = MongoClient('mongodb://sungin:jjang@3.39.193.123',27017)
db = client.dbjungle


##########################################################################
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)

app.json = CustomJSONProvider(app)


@app.errorhandler(500)
def internal_server_error(error):
    return 'Internal Server Error: {}'.format(error), 500


# 서버부터 만들기-> 클라이언트 만들기, 대문자 소문자 의외로 상관없을지도..
# home 
@app.route('/')
def home():
    return render_template('newVer.html')


#데이터 조회
@app.route('/memo/read/', methods=['GET'])
def read_memo():
    memos = list(db.memos.find().sort('likes', -1))
    # for memo in memos:
    #     memo['_id'] = str(memo['_id'])
    # mongodb 에서 고유 id 는 ObjectId 타입이다.
    # 복잡한 이진 형식이라 문자열로 변환해야 클라가 처리 가능
    return jsonify({'result': 'success', 'memos': memos})


#데이터 생성
@app.route('/memo/read/', methods=['POST'])
def add_memo():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    memo_id = {'title': title_receive, 'content': content_receive, 'likes':0}
    db.memos.insert_one(memo_id)
    return jsonify({'result':'success' })


#데이터 삭제
@app.route('/memo/delete/',methods=['POST'])
def delete_memo():
    memo_id = request.form['memo_id']
    db.memos.delete_one({'_id':ObjectId(memo_id)})
    return jsonify({'result':'success', 'msg':'삭제성공'})

#데이터 좋아요
@app.route('/memo/like/', methods=['POST'])
def like_memo():
    memo_id = request.form['memo_id']

    target_star = db.memos.find_one({'_id':ObjectId(memo_id)})
    current_likes = target_star['likes']
    new_likes = current_likes + 1

    db.memos.update_one({'_id':ObjectId(memo_id)}, {'$set':{'likes':new_likes}})
    return jsonify({'result':'success'})
 
#데이터 수정
@app.route('/memo/update/', methods=['POST'])
def update_memo():
    memo_id = request.form['memo_id']
    title_receive = request.form['title']
    content_receive = request.form['content']
    db.memos.update_one({'_id':ObjectId(memo_id)}, {'$set':{'title': title_receive, 'content': content_receive}})
    return jsonify({'result':'success'})



if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
