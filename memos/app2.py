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


# 서버부터 만들기-> 클라이언트 만들기, 대문자 소문자 의외로 상관없을지도..
# home 
@app.route('/')
def home():
    return render_template('newMod.html')


#데이터 조회
@app.route('/memo/read/', methods=['GET'])
def read_memo():
    return
#데이터 생성
@app.route('/memo/read/', methods=['POST'])
def add_memo():
    return

#데이터 삭제
@app.route('/memo/delte/',methods=['POST'])
def delete_memo():
    return

#데이터 좋아요
@app.route('/memo/like/', methods=['POST'])
def like_memo():
    return

#데이터 수정
@app.route('/memo/update/', methods=['POST'])
def update_memo():
    return


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)
