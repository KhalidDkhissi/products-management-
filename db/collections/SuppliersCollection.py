from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from window.Alert import Alert


class SuppliersCollection:
    def __init__(self, db):
        self.collection: Collection = db['Suppliers']

    def create_supplier(self, supplier_data):
        try:
            result = self.collection.insert_one(supplier_data)
            print(f"Supplier created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create supplier. Error: {e}")
            return None

    def read_one(self, query):
        try:
            supplier = self.collection.find_one(query)
            if supplier:
                print("Supplier found:", supplier)
            else:
                print("No supplier matches the query.")
            return supplier
        except PyMongoError as e:
            print(f"Failed to read supplier. Error: {e}")
            return None

    def read_all(self):
        try:
            categories = self.collection.find()

            return categories
        
        except PyMongoError as e:
            print(f"Failed to read supplier Error: {e}")
            Alert("error", "Failed to read supplier Error")
            return None

    def update_supplier(self, query, update_data):
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"Supplier updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No supplier matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update supplier. Error: {e}")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"Supplier deleted. Count: {result.deleted_count}")
            else:
                print("No supplier matches the query.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete supplier. Error: {e}")
            return None
        
    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} suppliers")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete suppliers Error: {e}")
            Alert("error", "Failed to delete suppliers Error")
            return None