from pymongo.errors import PyMongoError
from window.Alert import Alert
from datetime import datetime


class TasksCollection:
    def __init__(self, db):
        if db is not None:
            self.collection = db['Tasks']
        else:
            Alert("warning", "DB not found, something was wrong try again")

    def create_task(self, task_data):
        try:
            date = datetime.now()
            date_str = date.strftime('%Y-%m-%d')
            task_data["created_at"] = date_str
            task_data["updated_at"] = date_str

            result = self.collection.insert_one(task_data)
            print(f"task created with ID: {result.inserted_id}")
            return {"_id": result.inserted_id, "task_name": task_data["task_name"]}
        except PyMongoError as e:
            print(f"Failed to create task. Error: {e}")
            Alert("error", "Failed to create task. Error")
            return None

    def read_one(self, query):
        try:
            task = self.collection.find_one(query)
            if task:
                print("task found:", task)
                return task
            else:
                print("No task matches the query.")
                Alert("warning", "No task matches the query.")
                return None
            
        except PyMongoError as e:
            print(f"Failed to read task. Error: {e}")
            Alert("error", "Failed to create task. Error")
            return None

    def read_all(self):
        try:
            tasks = self.collection.find()

            return tasks
        
        except PyMongoError as e:
            print(f"Failed to read tasks Error: {e}")
            Alert("error", "Failed to read tasks Error")
            return None
    
    def find_many(self, query):
        try:
            tasks = self.collection.find(query)
            return tasks
        except PyMongoError as e:
            print(f"Failed to read tasks Error: {e}")
            Alert("error", "Failed to read tasks Error")
            return None

    def update_task(self, query, update_data):
        try:
            date = datetime.now()
            date_str = date.strftime('%Y-%m-%d')
            update_data["updated_at"] = date_str

            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"task updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No task matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update task. Error: {e}")
            Alert("error", "Failed to update task. Error")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"task deleted. Count: {result.deleted_count}")
                return result.deleted_count
            else:
                print("No task matches the query.")
                Alert("error", "No task matches the query.")
                return None
        except PyMongoError as e:
            print(f"Failed to delete task. Error: {e}")
            Alert("error", "Failed to delete task. Error")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} tasks.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete tasks. Error: {e}")
            Alert("error", "Failed to delete tasks")
            return None