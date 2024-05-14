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

#####################################################################################



#html 보여주기
@app.route('/')
def home():
    return render_template('index.html')

#API

@app.route('/memo', methods=['POST'])
def post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {
        'title':title_receive,
        'content':content_receive,

    }
    db.memos.insert_one(doc)
    
    return jsonify({'result':'success','msg':'데이터넣기완료'})
    

@app.route('/memo', methods=['GET'])
def read():
    result = list(db.memos.find({}, {'_id':0}).sort('like',-1))
    return jsonify({'result':'success','memos': result})

# memo read and post 까지는 성공


@app.route('/memo', methods=['POST'])
def like():
    title_receive = request.form['title_give']
    
    target_likes= db.memos.find_one({'title':title_receive})
    current_likes = target_likes['likes']
    
    new_likes = current_likes + 1
    
    db.memos.update_one( {'title':title_receive}, {'$set':{'likes':new_likes}} )
    
    return jsonify({'msg': 'like'})
    
    
@app.route('/memo', methods=['POST'])
def delete():
    title_receive = request.form['title_give']
    db.memos.delete_one({'title': title_receive})
    return jsonify({'msg': '삭제'})   

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
# @app.route('/memo', methods=['GET'])
# def read_articles():
