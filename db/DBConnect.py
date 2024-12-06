from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from window.Alert import Alert
from config.Static import Static


class DBConnection:
    def __init__(self):
        
        self._static_ = Static()
        
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self._static_.get("url"))
            self.db = self.client[self._static_.get("database_name")]
            self.client.admin.command('ping')
            print("Successfully connected to the database: ", self._static_.get("database_name"))
        except ConnectionFailure as e:
            print(f"Failed to connect to the database. Error: {e}")
            Alert("error", "Failed to connect to the database Error")
            self.client = None
            self.db = None

    def close(self):
        if self.client:
            self.client.close()
            print("Connection closed.")