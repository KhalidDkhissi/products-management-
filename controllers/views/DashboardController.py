

from db.collections.ProductsCollection import ProductsCollection

class DashboardController:
    def __init__(self, this, db):

        self.this = this
        self._db_ = db

        self.products_collection = db['Products']
        self.tasks_collection = db['Tasks']
        self.jobpostings_collection = db['JobPostings']

        self.init_module()

    def init_module(self):
        data = {}

        data = {
            "Inventories": self.products_collection.count_documents({}),
            "Tasks": self.tasks_collection.count_documents({}),
            "Job Postings": self.jobpostings_collection.count_documents({})
        }

        self.this._data_ = data