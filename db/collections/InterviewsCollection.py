from pymongo.errors import PyMongoError
from bson import ObjectId

from window.Alert import Alert

class InterviewsCollection:
    def __init__(self, db):
        self.collection = db['Interviews']
        self.candidates_collection = db['Candidates']
        self.job_postings_collection = db['JobPostings']

    def create_interview(self, interview_data):
        try:
            candidate = self.candidates_collection.find_one({"candidate_name": interview_data["candidate_name"]})
            if candidate:
                interview_data["candidate_id"] = candidate["_id"]
            else:
                print(f"Candidate '{interview_data['candidate_name']}' not found.")
                return None

            del interview_data["candidate_name"]
            
            job_posting = self.job_postings_collection.find_one({"job_title": interview_data["job_posting"]})
            if job_posting:
                interview_data["job_posting_id"] = job_posting["_id"]
            else:
                print(f"Job posting '{interview_data['job_posting']}' not found.")
                return None

            del interview_data["job_posting"]

            # Insert the interview
            result = self.collection.insert_one(interview_data)
            print(f"interview created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create interview. Error: {e}")
            return None

    def read_one(self, query):
        try:
            # Find the interview based on the query
            interview = self.collection.find_one(query)
            if not interview:
                print("interview not found.")
                return None

            # Find the candidate name using the id
            candidate = self.candidates_collection.find_one({"_id": interview["candidate_id"]})
            if candidate:
                interview["candidate_name"] = candidate["candidate_name"]
            else:
                interview["candidate_name"] = None 

            del interview["candidate_id"]
            
            # Find the job title name using the id
            job_posting = self.job_postings_collection.find_one({"_id": interview["job_posting_id"]})
            if job_posting:
                interview["job_posting"] = job_posting["job_title"]
            else:
                interview["job_posting"] = None 

            del interview["job_posting_id"]

            return interview
        except PyMongoError as e:
            print(f"Failed to read interview. Error: {e}")
            return None
    
    def read_all(self):
        try:
            interviews = self.collection.find()  # Retrieve all interviews
            all_interviews = []
            
            for interview in interviews:
                candidate = self.candidates_collection.find_one({"_id": interview["candidate_id"]})
                if candidate:
                    interview["candidate_name"] = candidate["candidate_name"]
                else:
                    interview["candidate_name"] = None 

                del interview["candidate_id"]

                job_posting = self.job_postings_collection.find_one({"_id": interview["job_posting_id"]})
                if job_posting:
                    interview["job_posting"] = job_posting["job_title"]
                else:
                    interview["job_posting"] = None 

                del interview["job_posting_id"]

                # Add the processed interview to the list
                all_interviews.append(interview)

            return all_interviews
        except PyMongoError as e:
            print(f"Failed to read interviews. Error: {e}")
            return None

    def update_interview(self, query, update_data):
        try:
            if "candidate_name" in update_data:
                candidate = self.candidates_collection.find_one({"candidate_name": update_data["candidate_name"]})
                if candidate:
                    update_data["candidate_name"] = candidate["_id"]
                else:
                    print(f"Candidate '{update_data['candidate_name']}' not found.")
                    return None 

                del update_data["candidate_name"]
                del query["candidate_name"]

            if "job_posting" in update_data:
                job_posting = self.job_postings_collection.find_one({"job_title": update_data["job_posting"]})
                if job_posting:
                    update_data["job_posting_id"] = ObjectId(job_posting["_id"])
                    query["job_posting_id"] = ObjectId(job_posting["_id"])
                else:
                    print(f"Job posting '{update_data['job_posting']}' not found.")
                    return None
                
                del update_data["job_posting"]
                del query["job_posting"]

            # Update the interview
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"interview updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No interview matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update interview. Error: {e}")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)

            if result.deleted_count > 0:
                print(f"interview deleted. Count: {result.deleted_count}")
            else:
                print("No interview matches the query.")
            return result.deleted_count
        
        except PyMongoError as e:
            print(f"Failed to delete interview. Error: {e}")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)

            print(f"Deleted {result.deleted_count} interviews.")
            return result.deleted_count

        except PyMongoError as e:
            print(f"Failed to delete interviews. Error: {e}")
            Alert("error", "Failed to delete interviews. Error")
            return None
