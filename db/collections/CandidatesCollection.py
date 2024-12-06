from pymongo.errors import PyMongoError
from bson import ObjectId

from window.Alert import Alert

class CandidatesCollection:
    def __init__(self, db):
        self.collection = db['Candidates']
        self.job_postings_collection = db['JobPostings']

    def create_candidate(self, candidate_data):
        try:
            job_posting = self.job_postings_collection.find_one({"job_title": candidate_data["job_posting"]})
            if job_posting:
                candidate_data["job_posting_id"] = job_posting["_id"]
            else:
                print(f"Job posting '{candidate_data['job_posting']}' not found.")
                return None

            del candidate_data["job_posting"]

            # Insert the candidate
            result = self.collection.insert_one(candidate_data)
            print(f"candidate created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create candidate. Error: {e}")
            return None

    def read_one(self, query):
        try:
            # Find the candidate based on the query
            candidate = self.collection.find_one(query)
            if not candidate:
                print("candidate not found.")
                return None

            # Find the job title name using the id
            job_posting = self.job_postings_collection.find_one({"_id": candidate["job_posting_id"]})
            if job_posting:
                candidate["job_posting"] = job_posting["job_title"]
            else:
                candidate["job_posting"] = None 

            del candidate["job_posting_id"]

            return candidate
        except PyMongoError as e:
            print(f"Failed to read candidate. Error: {e}")
            return None
    
    def read_all(self):
        try:
            candidates = self.collection.find()  # Retrieve all candidates
            all_candidates = []
            
            for candidate in candidates:
                # Find the job title using the job_id
                job_posting = self.job_postings_collection.find_one({"_id": candidate["job_posting_id"]})
                if job_posting:
                    candidate["job_posting"] = job_posting["job_title"]
                else:
                    candidate["job_posting"] = None 

                del candidate["job_posting_id"]

                # Add the processed candidate to the list
                all_candidates.append(candidate)

            return all_candidates
        except PyMongoError as e:
            print(f"Failed to read candidates. Error: {e}")
            return None

    def update_candidate(self, query, update_data):
        try:
            # If job_posting is provided, find the corresponding job_id
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

            # Update the candidate
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"candidate updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No candidate matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update candidate. Error: {e}")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)

            if result.deleted_count > 0:
                print(f"candidate deleted. Count: {result.deleted_count}")
            else:
                print("No candidate matches the query.")
            return result.deleted_count
        
        except PyMongoError as e:
            print(f"Failed to delete candidate. Error: {e}")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)

            print(f"Deleted {result.deleted_count} candidates.")
            return result.deleted_count

        except PyMongoError as e:
            print(f"Failed to delete candidates. Error: {e}")
            Alert("error", "Failed to delete candidates. Error")
            return None
