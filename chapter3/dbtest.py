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


# MongoDB에서 데이터 모두 보기
all_users = list(db.firstCollection.find({}))

# 참고) MongoDB에서 특정 조건의 데이터 모두 보기
same_ages = list(db.firstCollection.find({'age':21}))

# print(all_users[0])         # 0번째 결과값을 보기
# print(all_users[0]['name']) # 0번째 결과값의 'name'을 보기

# for user in all_users:      # 반복문을 돌며 모든 결과값을 보기
#     print(user)
    
# user = db.firstCollection.find_one({'name':'bobby'})
# print(user)

# # 그 중 특정 키 값을 빼고 보기
# user = db.firstCollection.find_one({'name':'bobby'},{'_id':False}) # _ 는 제외한다는뜻
# print(user)    
    
    
# 생김새
# db.people.update_many(찾을조건,{ '$set': 어떻게바꿀지 })

# 예시 - 오타가 많으니 이 줄을 복사해서 씁시다!
# db.firstCollection.update_one({'name':'bobby'},{'$set':{'age':19}})

user = db.firstCollection.find_one({'name':'bobby'})
print(user)    

db.firstCollection.delete_one({'name':'bobby'})

user = db.firstCollection.find_one({'name':'bobby'})
print(user)
    