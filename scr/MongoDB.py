import pymongo
from pymongo import MongoClient
import json

class MongoDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['DOAN']
        self.collection = self.db['bases']

    def read_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def insert_data(self, data):
        self.collection.insert_many(data)

    def print_data(self):
        for data in self.collection.find():
            print(data)
    def read_data(self):
        return self.collection.find()
    #truy van
    def query_data(self, query):
        return self.collection.find(query)

    # sắp xếp
    def sort_data(self, key, value):
        return self.collection.find().sort(key, value)

    def close_connection(self):
        self.client.close()

