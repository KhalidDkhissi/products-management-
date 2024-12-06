from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson import ObjectId
from datetime import datetime

from window.Alert import Alert

class OrdersCollection:
    def __init__(self, db):
        self.collection = db['Orders']
        self.products_collection = db['Products']

    def create_order(self, order_data):
        try:
            all_products = order_data["products"].copy()
            
            for product_item in all_products:
                product = self.products_collection.find_one({"product_name": product_item["product_name"]})
            
                if product:
                    product_item["product_id"] = product["_id"]
                else:
                    print(f"Category '{product_item['product_name']}' not found.")
                    return None

                del product_item["product_name"]
                del product_item["price"]
            
            # order_data["customer_name"] = f"{order_data['first_name']} {order_data['last_name']}"

            order_data["products"] = all_products
            order_data["payment_status"] = "Pending"
            order_data["shipping_status"] = "Pending"

            now = datetime.now()
            creation_date = now.strftime("%Y-%m-%d %H:%M:%S")
            order_data["creation_date"] = creation_date 
            
            print("order_data: ", order_data)
            # Insert the product
            result = self.collection.insert_one(order_data)
            print(f"Product created with ID: {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            print(f"Failed to create product. Error: {e}")
            return None

    def read_one(self, query):
        try:
            # Find the order based on the query
            order = self.collection.find_one(query)
            
            if not order:
                print("Product not found.")
                return None

            all_products = []

            for product_item in order["products"]:
                product = self.products_collection.find_one({"_id": product_item["product_id"]})
                
                if product:
                    product_item["product_name"] = product["product_name"]
                    product_item["price"] = product["selling_price"]
                else:
                    product_item["product_name"] = None  # Handle missing product
                    product_item["price"] = None  # Handle missing product

                del product_item["product_id"]

                all_products.append(product_item)

            order["products"] = all_products

            return order
        except PyMongoError as e:
            print(f"Failed to read product. Error: {e}")
            return None
    
    def read_all(self):
        try:
            orders = self.collection.find()  # Retrieve all products
            
            all_orders = []
            
            for order in orders:
                # Find the product name using the product_id
                all_products = []

                for product_item in order["products"]:
                    product = self.products_collection.find_one({"_id": product_item["product_id"]})
                    
                    if product:
                        product_item["product_name"] = product["product_name"]
                        product_item["price"] = product["selling_price"]
                    else:
                        product_item["product_name"] = None  # Handle missing product
                        product_item["price"] = None  # Handle missing product

                    del product_item["product_id"]

                    all_products.append(product_item)

                order["products"] = all_products
                
                all_orders.append(order)

            return all_orders
        
        except PyMongoError as e:
            print(f"Failed to read orders. Error: {e}")
            return None

    def update_order(self, _q, _uq):
        try:
            # If product_name is provided, find the corresponding product_id
            query = _q.copy()
            update_data = _uq.copy()
            
            if "products" in update_data:

                all_products = []

                for product_item in update_data["products"]:
                    if "product_name" in product_item:
                        product = self.products_collection.find_one({"product_name": product_item["product_name"]})
                        
                        if product:
                            product_item["product_id"] = ObjectId(product["_id"])
                        else:
                            product_item["product_id"] = None  # Handle missing product

                        del product_item["product_name"]
                        del product_item["price"]

                        all_products.append(product_item)

                update_data["products"] = all_products
            
            if "products" in query:

                all_products = []

                for product_item in query["products"]:
                    if "product_name" in product_item:
                        product = self.products_collection.find_one({"product_name": product_item["product_name"]})
                        
                        if product:
                            product_item["product_id"] = ObjectId(product["_id"])
                        else:
                            product_item["product_id"] = None  # Handle missing product

                        del product_item["product_name"]
                        del product_item["price"]

                        all_products.append(product_item)

                query["products"] = all_products

            print("\nquery: ", query)

            print("\nupdate data: ", update_data)

            # Update the order
            result = self.collection.update_one(query, {'$set': update_data})
            
            if result.matched_count > 0:
                print(f"Order updated. Matched: {result.matched_count}, Modified: {result.modified_count}")
                return result
            else:
                Alert("error", "No order matches the query.")
            return result.modified_count
        except PyMongoError as e:
            print(f"Failed to update order. Error: {e}")
            return None

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)

            if result.deleted_count > 0:
                print(f"Order deleted. Count: {result.deleted_count}")
            else:
                print("No order matches the query.")

            return result.deleted_count
        
        except PyMongoError as e:
            print(f"Failed to delete order. Error: {e}")
            return None

    def delete_all(self, query):
        try:
            result = self.collection.delete_many(query)

            print(f"Deleted {result.deleted_count} orders.")
            
            return result.deleted_count
        except PyMongoError as e:
            print(f"Failed to delete orders. Error: {e}")
            Alert("error", "Failed to delete orders. Error")
            return None
