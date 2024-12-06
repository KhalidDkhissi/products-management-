from pymongo.errors import PyMongoError
from window.Alert import Alert


class UsersCollection:
    def __init__(self, db):
        if db is not None:
            self.collection = db['Users']
        else:
            Alert("warning", "DB not found, something was wrong try again")

    def create_user(self, user_data):
        try:
            result = self.collection.insert_one(user_data)
            print(f"user created with ID: {result.inserted_id}")
            return {"_id": result.inserted_id, "full_name": user_data["full_name"]}
        except PyMongoError as e:
            print(f"Failed to create user. Error: {e}")
            Alert("error", "Failed to create user. Error")
            return None

    def read_one(self, query):
        try:
            user = self.collection.find_one(query)
            if user:
                print("user found:", user)
                return user
            else:
                print("No user matches the query.")
                Alert("warning", "No user matches the query.")
                return None
            
        except PyMongoError as e:
            print(f"Failed to read user. Error: {e}")
            Alert("error", "Failed to create user. Error")
            return None

    def read_all(self):
        try:
            categories = self.collection.find()

            return categories
        
        except PyMongoError as e:
            print(f"Failed to read categories Error: {e}")
            Alert("error", "Failed to read categories Error")
            return None

    def update_user(self, query, update_data):
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"user updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No user matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update user. Error: {e}")
            Alert("error", "Failed to update user. Error")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"user deleted. Count: {result.deleted_count}")
                return True
            else:
                print("No user matches the query.")
                Alert("error", "No user matches the query.")
                return None
        except PyMongoError as e:
            print(f"Failed to delete user. Error: {e}")
            Alert("error", "Failed to delete user. Error")
            return None

    def delete_all(self):
        try:
            result = self.collection.delete_many({})
            print(f"Deleted {result.deleted_count} users.")
            return True
        except PyMongoError as e:
            print(f"Failed to delete users. Error: {e}")
            Alert("error", "Failed to delete users")
            return None