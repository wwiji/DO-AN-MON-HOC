
from pymongo import MongoClient
import json


class Database:
    def __init__(self, db_name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
    # Insert data vào database
    def insert_many(self, data):
        self.db.insert_many(data)

    # Đếm số lượng bản ghi
    def count_documents(self):
        return self.db.count_documents({})
    
    # Tạo collection
    def create_collection(self, collection_name):
        self.db.create_collection(collection_name)
    
    # Xóa collection
    def drop_collection(self, collection_name):
        self.db.drop_collection(collection_name)

    def delete_many(self, collection_name, query):
        self.db[collection_name].delete_many(query)

    # tìm kiếm theo điều kiện
    def find(self, collection_name, query):
        return self.db[collection_name].find(query)
    
    # sắp xếp theo điều kiện
    def sort(self, collection_name, query): 
        return self.db[collection_name].find().sort(query)

    # cập nhật theo điều kiện
    def update_many(self, collection_name, query, new_values):
        return self.db[collection_name].update_many(query, new_values)

    # đếm số lượng bản ghi
    def count_documents(self, collection_name, query):
        return self.db[collection_name].count_documents(query)
    
# Tạo đối tượng database
db = Database("CSDM")

# Đọc file json
with open("data.json", "r") as file:
    data = json.load(file)
