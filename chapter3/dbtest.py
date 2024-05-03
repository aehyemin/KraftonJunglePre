from pymongo import MongoClient
client = MongoClient('localhost', 27017)
#mongoDB는 27017 포트로 돌아감
db = client.jungle
# jungle 이라는 이름의 db 를 만든다.

name = db.list_collection_names()

print(name)
#MongoDB에insert 하기
#'firstCollection'이라는 collection에 { }디렉토리를 넣음
# db.firstCollection.insert_one({'name':'bobby', 'age':21})
# db.firstCollection.insert_one({'name':'kay', 'age':27})
# db.firstCollection.insert_one({'name':'hyem', 'age':30})

#MongoDB에서 데이터 모두 보기
all_data = list(db.firstCollection.find({}))

same_ages = list(db.firstCollection.find({'age':21}))

# print(all_data[0])
# print(all_data[0]['name'])

# for data in all_data:
#     print(data)

#특정 결과 값 뽑아보기
# data = db.firstColletion.find({'name':'john'})
# print(data)

# data = db.firstColletion.find_one({'name':'bobby'}, {'_id':False})
# print(data)

# 생김새
# db.people.update_many(찾을조건,{ '$set': 어떻게바꿀지 })

# 예시 - 오타가 많으니 이 줄을 복사해서 씁시다!


# data = db.firstColletion.find_one({'name':'kay'})
data = db.firstColletion.find_one({'name':'kay'})

for data in all_data:
    print(data)

# data = db.firstCollection.find_one({'name':'hyem'})
# print(data)