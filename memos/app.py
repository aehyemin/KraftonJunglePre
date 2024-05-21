from bson import ObjectId
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys

app = Flask(__name__)

client = MongoClient('localhost',27017)
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

#html 보여주기
@app.route('/')
def home():
    return render_template('index1.html')


# 메모 목록을 조회하고 반환(데이터 조회)
@app.route('/memo/list', methods=['GET'])
def read():
    memos = list(db.memos.find().sort('likes',-1))
    for memo in memos:
        memo['_id'] = str(memo['_id'])
    return jsonify({'result':'success','memos': memos})


# 새로운 메모를 추가(데이터 생성)
@app.route('/memo/list', methods=['POST'])
def add_memo():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    memo_id = {'title':title_receive, 'content':content_receive, 'likes':0}
    db.memos.insert_one(memo_id)
    
    return jsonify({'result':'success'})



# memo read and post 까지는 성공

# 좋아요 API
@app.route('/memo/like', methods=['POST'])
def like_memo():
    memo_id = request.form['memo_id']
    
    target_star = db.memos.find_one({'_id': ObjectId(memo_id)})
    current_like = target_star['likes']
    new_like = current_like + 1

    db.memos.update_one({'_id': ObjectId(memo_id)}, {'$set': {'likes': new_like}})

    return jsonify({'result': 'success'})



# 수정 api
@app.route('/memo/update', methods=['POST'])
def update_memo():
    memo_id = request.form['memo_id']
    # update_receive = request.form['update_give']
    title_receive = request.form['title']
    content_receive = request.form['content']
    db.memos.update_one({'_id': ObjectId(memo_id)}, {'$set': {'title': title_receive,'content':content_receive}})
    return jsonify({'result': 'success'})


# 삭제 API
@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    memo_id = request.form['memo_id']
    db.memos.delete_one({'_id':ObjectId(memo_id)})
    return jsonify({'result':'success', 'msg':'삭제성공'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
