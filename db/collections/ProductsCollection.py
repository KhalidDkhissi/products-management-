from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson import ObjectId

from window.Alert import Alert

class ProductsCollection:
    def __init__(self, db):
        self.collection = db['Products']
        self.categories_collection = db['Categories']
        self.suppliers_collection = db['Suppliers']

    def create_product(self, product_data):
        try:
            # Find category_id by category_name
            category = self.categories_collection.find_one({"category_name": product_data["category_name"]})
            if category:
                product_data["category_id"] = category["_id"]
            else:
                print(f"Category '{product_data['category_name']}' not found.")
                return None

            # Find supplier_id by supplier_name
            supplier = self.suppliers_collection.find_one({"lieferant_name": product_data["lieferant_name"]})
            if supplier:
                product_data["supplier_id"] = supplier["_id"]
            else:
                print(f"Supplier '{product_data['lieferant_name']}' not found.")
                return None

            # Remove category_name and supplier_name from product_data
            del product_data["category_name"]
            del product_data["lieferant_name"]

            # Insert the product
            result = self.collection.insert_one(product_data)
            print(f"Product created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create product. Error: {e}")
            return None

    def read_one(self, query):
        try:
            # Find the product based on the query
            product = self.collection.find_one(query)
            if not product:
                print("Product not found.")
                return None

            # Find the category name using the category_id
            category = self.categories_collection.find_one({"_id": product["category_id"]})
            if category:
                product["category_name"] = category["category_name"]
            else:
                product["category_name"] = None  # Handle missing category

            # Find the supplier name using the supplier_id
            supplier = self.suppliers_collection.find_one({"_id": product["supplier_id"]})
            if supplier:
                product["lieferant_name"] = supplier["lieferant_name"]
            else:
                product["lieferant_name"] = None  # Handle missing supplier

            # Remove category_id and supplier_id from the product data
            del product["category_id"]
            del product["supplier_id"]

            return product
        except PyMongoError as e:
            print(f"Failed to read product. Error: {e}")
            return None
    
    def read_all(self):
        try:
            products = self.collection.find()  # Retrieve all products
            all_products = []
            
            for product in products:
                # Find the category name using the category_id
                category = self.categories_collection.find_one({"_id": product["category_id"]})
                if category:
                    product["category_name"] = category["category_name"]
                else:
                    product["category_name"] = None  # Handle missing category

                # Find the supplier name using the supplier_id
                supplier = self.suppliers_collection.find_one({"_id": product["supplier_id"]})
                if supplier:
                    product["lieferant_name"] = supplier["lieferant_name"]
                else:
                    product["lieferant_name"] = None  # Handle missing supplier

                # Remove category_id and supplier_id from the product data
                del product["category_id"]
                del product["supplier_id"]

                # Add the processed product to the list
                all_products.append(product)

            return all_products
        except PyMongoError as e:
            print(f"Failed to read products. Error: {e}")
            return None

    def update_product(self, query, update_data):
        try:
            # If category_name is provided, find the corresponding category_id
            if "category_name" in update_data:
                category = self.categories_collection.find_one({"category_name": update_data["category_name"]})
                if category:
                    update_data["category_id"] = ObjectId(category["_id"])
                    query["category_id"] = ObjectId(category["_id"])
                else:
                    print(f"Category '{update_data['category_name']}' not found.")
                    return None
                del update_data["category_name"]
                del query["category_name"]

            # If supplier_name is provided, find the corresponding supplier_id
            if "lieferant_name" in update_data:
                supplier = self.suppliers_collection.find_one({"lieferant_name": update_data["lieferant_name"]})
                if supplier:
                    update_data["supplier_id"] = ObjectId(supplier["_id"])
                    query["supplier_id"] = ObjectId(supplier["_id"])
                else:
                    print(f"Supplier '{update_data['lieferant_name']}' not found.")
                    return None
                del update_data["lieferant_name"]
                del query["lieferant_name"]

            # Update the product
            result = self.collection.update_one(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"Product updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
            else:
                print("No product matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update product. Error: {e}")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"Product deleted. Count: {result.deleted_count}")
            else:
                print("No product matches the query.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete product. Error: {e}")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} products.")
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete products. Error: {e}")
            Alert("error", "Failed to delete products. Error")
            return None
