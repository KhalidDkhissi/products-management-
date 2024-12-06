from pymongo.errors import PyMongoError
from window.Alert import Alert

class AdminsCollection:
    def __init__(self, db):
        if db is not None:
            self.collection = db['Admins']
        else:
            Alert("warning", "DB not found, something was wrong try again")

    def create_admin(self, admin_data):
        try:
            result = self.collection.insert_one(admin_data)
            print(f"admin created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create admin. Error: {e}")
            Alert("error", "Failed to create admin. Error")
            return None

    def read_one(self, query):
        try:
            admin = self.collection.find_one(query)
            if admin:
                print("admin found:", admin)
                return admin
            else:
                print("No admin matches the query.")
                Alert("warning", "No admin matches the query.")
                return None
            
        except PyMongoError as e:
            print(f"Failed to read admin. Error: {e}")
            Alert("error", "Failed to create admin. Error")
            return None

    def read_all(self):
        try:
            admins = self.collection.find()

            return admins
        
        except PyMongoError as e:
            print(f"Failed to read admins Error: {e}")
            Alert("error", "Failed to read admins Error")
            return None

    def update_admin(self, query, update_data):
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"admin updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No admin matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update admin. Error: {e}")
            Alert("error", "Failed to update admin. Error")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"admin deleted. Count: {result.deleted_count}")
                return result.deleted_count
            else:
                print("No admin matches the query.")
                Alert("error", "No admin matches the query.")
                return None
        except PyMongoError as e:
            print(f"Failed to delete admin. Error: {e}")
            Alert("error", "Failed to delete admin. Error")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} admins.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete admins. Error: {e}")
            Alert("error", "Failed to delete admins")
            return None