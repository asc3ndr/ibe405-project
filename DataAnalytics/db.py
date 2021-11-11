from pymongo import MongoClient

# Basic DB connection
class DB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.ibe
        self.weatherdata = self.db.weatherdata

    def create(self, data: dict):
        return self.weatherdata.insert_one(data)

    def read(self):
        return self.weatherdata.find({})

    def get(self, datetime: str):
        return self.weatherdata.find_one({"_id": datetime})
