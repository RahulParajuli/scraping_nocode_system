from pymongo import MongoClient

from autoproject.settings import MONGO_COLLECTION, MONGO_CONNECTION_STRING, MONGODB


class MongoUtil:
    
    def __init__(self):
        self.connection_str = MONGO_CONNECTION_STRING
        self.client = MongoClient(self.connection_str)
        self.db_handle = self.get_db_handle(MONGODB)
    
    def get_db_handle(self, db_name):
        db_handle = self.client[db_name]
        return db_handle
    
    def get_item(self, query):
        collection_handle = self.db_handle[MONGO_COLLECTION]
        data = collection_handle.find({"search_term": query})
        return data
    
    def insert_data(self, data, query):
        try:
            for data_item in data:
                data_item["search_term"] = query
                collection_handle = self.db_handle[MONGO_COLLECTION]
                collection_handle.insert_one(data_item)
            return True
        except Exception as e:
            return False
     
           
            
if __name__ == "__main__":
    astt = MongoUtil()
    astt = astt.get_item("educational institutions in Northern Ireland")