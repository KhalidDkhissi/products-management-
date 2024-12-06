from PyQt5.QtCore import QRegExp

class Static:
    def __init__(self):
        self._static_ = {
            "app_name": "Management Suite System",
            "url": "mongodb+srv://khaliddkhissi21:ugnYAkDj4AtFQw0s@cluster0.ifyh9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            "database_name":"MangSuiteSystem",
            "sm_menu" : 50,
            "lg_menu" : 300,
            "state_menu" : True,
            "current_view" : "dashboard",
            "index_view" : 0,
            "per_grid": 3,
            "items_side_menu": {
                "dashboard": [],
                "inventory": ["Products", "Categories", "Orders", "Suppliers", "Transactions"],
                "tasks": [],
                "recruitment": ["Job Postings", "Candidates", "Interviews"],
                "help": [],
                "settings": [],
            },
            "role_users" : ["Directeur", "Product Manager", "General Accounting", "Designer ux ui", "Full Stack Dev", "Engineering"],
            "accept_files": ["xlsm", "xlsx", "csv"],
            "regex_text": QRegExp("[a-z-A-Zéàèç0-9_/)( ]+"),
            "regex_number": QRegExp("[0-9]+"),
            "thead_tables": {
                "products": {
                    "thead": ["Product name", "Category name", "Lieferant name", "Quantity", "Wholesale price", "Selling price", "Actions"],
                    "size": [0.3, 0.3, 0.3, 0.2, 0.3, 0.2, 0.2],
                },
                "categories": {
                    "thead": ["Category name", "Description", "Actions"],
                    "size": [0.3, 1.3, 0.3],
                },
                "suppliers": {
                    "thead": ["Lieferant name", "Contact person", "Email", "Phone number", "Address", "Actions"],
                    "size": [0.3, 0.2, 0.4, 0.3, 0.4, 0.2],
                },
                "orders": {
                    "thead": ["_ID", "Creation Date", "Customer name", "Payment status", "Shipping status", "Total", "Actions"],
                    "size": [0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2],
                },
                "transactions": {
                    "thead": ["Product name", "Transactions type", "Quantity", "Transactions date", "Actions"],
                    "size": [0.4, 0.4, 0.2, 0.4, 0.3],
                },
                "tasks": {
                    "thead": ["Task name", "Description", "Priority", "Status", "Due date", "Created at", "Actions"],
                    "size": [0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2],
                },
                "job postings": {
                    "thead": ["job title", "department", "job description", "requirements", "posted date", "closing date", "status", "Actions"],
                    "size": [0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2],
                },
                "candidates": {
                    "thead": ["candidate name", "email", "phone number", "resume link", "job posting", "application date", "status", "Actions"],
                    "size": [0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                },
                "interviews": {
                    "thead": ["candidate name", "job posting", "interview date", "interviewer", "status", "notes", "Actions"],
                    "size": [0.3, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2],
                },
            },
            "company_info": {
                "name": "Managment Suite System",
                "address": "Berlin - Germany",
                "phone_number": "(+44)123456789",
                "stadt": "Bonn"
            },
            "priority": ["High", "Medium", "Low"],
            "status": ["Pending", "In Progress", "Completed"],
            "status_jobs": ["Open", "Closed"],
            "status_candidates": ["Applied", "Interview Scheduled", "Hired", "Rejected"],
            "status_interviews": ["Scheduled", "Completed", "Cancelled"],
            "transactions_type": ["IN", "OUT"],
            "payment_status": ["Pending", "Paid", "Declined", "Canceled"],
            "shipping_status": ["Pending", "Processing", "Shipped", "Delivered", "Canceled"],
            
            "intro": """     Welcome to the ProManage Suite, a comprehensive management tool designed to streamline your business operations. 
This application integrates various management systems into a single platform, allowing for efficient handling of inventory tasks,
and HR recruitment processes. The ProManage Suite empowers you to monitor and manage these key areas from one convenient dashboard, 
improving productivity and organizational efficiency."""   ,
            
            "inventory": """     The Inventory Management module allows you to keep track of your products, suppliers, and inventory 
transactions with ease. This system provides real-time data on stock levels, helps manage reorders, and offers detailed insights
into product categories. With our intuitive interface, you can quickly access inventory details, monitor stock levels, and ensure
that your supply chain operates smoothly.""",
            
            "task": """     The Task Management module is designed to help you organize and prioritize your daily tasks.
It enables you to create, assign, and monitor tasks, ensuring that nothing falls through the cracks. The system provides 
a clear overview of task statuses, deadlines, and priorities, allowing you to manage workloads effectively and ensure timely 
completion of all critical activities.""",
            
            "recruitment": """     The HR Recruitment Management module simplifies the hiring process by providing tools to manage 
job postings, candidates, and interviews. This system helps you track candidates throughout the recruitment pipeline, schedule 
interviews, and monitor the status of job postings. By streamlining these processes, the module ensures that your recruitment 
efforts are efficient and effective.""",

        }

        self._static_["width_menu"] = self._static_["lg_menu"]

    def get(self, key):
        if key in self._static_:
            return self._static_[key]
        
        return None
    
    def set(self, key, value):
        self._static_[key] = value