from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson import ObjectId
from window.Alert import Alert



class TransactionsCollection:
    def __init__(self, db):
        self.collection = db['Transactions']
        self.products_collection = db['Products']

    def create_transaction(self, transaction_data):
        try:
            product = self.products_collection.find_one({"product_name": transaction_data["product_name"]})
            if product:
                transaction_data["product_id"] = product["_id"]
            else:
                print(f"Product '{transaction_data['product_name']}' not found.")
                return None
            
            del transaction_data["product_name"]

            result = self.collection.insert_one(transaction_data)

            print(f"Transaction created with ID: {result.inserted_id}")
            
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create transaction. Error: {e}")
            return None

    def read_one(self, query):
        try:
            transaction_data = self.collection.find_one(query)
            if not transaction_data:
                print("No transaction matches the query.")

            product = self.products_collection.find_one({"_id": transaction_data["product_id"]})
            
            if product:
                transaction_data["product_name"] = product["product_name"]
            else:
                print(f"Product '{product['product_name']}' not found.")
                return None
            
            del transaction_data["product_id"]

            return transaction_data
        
        except PyMongoError as e:
            print(f"Failed to read transaction. Error: {e}")
            return None

    def read_all(self):
        try:
            transactions = self.collection.find()

            all_transactions = []

            for transaction in transactions:
                product = self.products_collection.find_one({"_id": transaction["product_id"]})
            
                if product:
                    transaction["product_name"] = product["product_name"]
                else:
                    print(f"Product '{product['product_name']}' not found.")
                    return None
                
                del transaction["product_id"]

                all_transactions.append(transaction)

            return all_transactions        

        except PyMongoError as e:
            print(f"Failed to read transactions. Error: {e}")
            return None

    def update_transaction(self, query, update_data):
        try:
            if "product_name" in update_data:

                product = self.products_collection.find_one({"product_name": update_data["product_name"]})
                
                if product:
                    update_data["product_id"] = ObjectId(product["_id"])
                    query["product_id"] = ObjectId(product["_id"])
                    
                    del update_data["product_name"]
                    del query["product_name"]

                else:
                    print(f"Product '{update_data['product_name']}' not found.")
                    return None
            else:
                print(f"Category '{update_data['category_name']}' not found.")
                return None

            result = self.collection.update_one(query, {'$set': update_data})

            if result.matched_count > 0:
                print(f"Transaction updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No transaction matches the query.")

            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update transaction. Error: {e}")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"Transaction deleted. Count: {result.deleted_count}")
            else:
                print("No transaction matches the query.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete transaction. Error: {e}")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} transactions.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete transactions. Error: {e}")
            Alert("error", "Failed to delete transactions. Error")
            return None