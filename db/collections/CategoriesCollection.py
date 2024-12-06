from pymongo.errors import PyMongoError
from window.Alert import Alert

class CategoriesCollection:
    def __init__(self, db):
        if db is not None:
            self.collection = db['Categories']
        else:
            Alert("warning", "DB not found, something was wrong try again")

    def create_category(self, category_data):
        try:
            result = self.collection.insert_one(category_data)
            print(f"Category created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create category. Error: {e}")
            Alert("error", "Failed to create category. Error")
            return None

    def read_one(self, query):
        try:
            category = self.collection.find_one(query)
            if category:
                print("Category found:", category)
                return category
            else:
                print("No category matches the query.")
                Alert("warning", "No category matches the query.")
                return None
            
        except PyMongoError as e:
            print(f"Failed to read category. Error: {e}")
            Alert("error", "Failed to create category. Error")
            return None

    def read_all(self):
        try:
            categories = self.collection.find()

            return categories
        
        except PyMongoError as e:
            print(f"Failed to read categories Error: {e}")
            Alert("error", "Failed to read categories Error")
            return None

    def update_category(self, query, update_data):
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"Category updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No category matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update category. Error: {e}")
            Alert("error", "Failed to update category. Error")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"Category deleted. Count: {result.deleted_count}")
                return result.deleted_count
            else:
                print("No category matches the query.")
                Alert("error", "No category matches the query.")
                return None
        except PyMongoError as e:
            print(f"Failed to delete category. Error: {e}")
            Alert("error", "Failed to delete category. Error")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} categories.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete categories. Error: {e}")
            Alert("error", "Failed to delete categories")
            return None