from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["CSDM"]

# tạo ra 10 bảng
for i in range(10):
    db.create_collection(f"table_{i}")

#Doc file json
with open("data.json", "r") as file:
    data = json.load(file)

#Insert data vào database
db.insert_many(data)

#In ra số lượng bản ghi trong database
print(db.count_documents({}))   

