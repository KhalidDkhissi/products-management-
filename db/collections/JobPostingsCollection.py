from pymongo.errors import PyMongoError
from window.Alert import Alert

class JobPostingsCollection:
    def __init__(self, db):
        if db is not None:
            self.collection = db['JobPostings']
        else:
            Alert("warning", "DB not found, something was wrong try again")

    def create_job_posting(self, job_data):
        try:
            result = self.collection.insert_one(job_data)
            print(f"Job posting created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create job posting. Error: {e}")
            Alert("error", "Failed to create job posting. Error")
            return None

    def read_one(self, query):
        try:
            job_posting = self.collection.find_one(query)
            if job_posting:
                print("job posting found:", job_posting)
                return job_posting
            else:
                print("No job posting matches the query.")
                Alert("warning", "No job_posting matches the query.")
                return None
            
        except PyMongoError as e:
            print(f"Failed to read job posting. Error: {e}")
            Alert("error", "Failed to create job posting. Error")
            return None

    def read_all(self):
        try:
            jobsPosting = self.collection.find()

            return jobsPosting
        
        except PyMongoError as e:
            print(f"Failed to read jobs posting Error: {e}")
            Alert("error", "Failed to read jobs posting Error")
            return None

    def update_job_posting(self, query, update_data):
        try:
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"job posting updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No job posting matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update job posting. Error: {e}")
            Alert("error", "Failed to update job posting. Error")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"job posting deleted. Count: {result.deleted_count}")
                return result.deleted_count
            else:
                print("No job posting matches the query.")
                Alert("error", "No job_posting matches the query.")
                return None
        except PyMongoError as e:
            print(f"Failed to delete job posting. Error: {e}")
            Alert("error", "Failed to delete job posting. Error")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} jobs posting.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete jobs posting. Error: {e}")
            Alert("error", "Failed to delete jobs posting")
            return None