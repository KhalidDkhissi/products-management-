import os
from pathlib import Path
from reportlab.lib.pagesizes import A4 #reportlab library is used for defining the size of pages when creating PDFs.
from reportlab.pdfgen import canvas #pdfgen is a module that deals with PDF generation, contains classes and methods specifically for creating and manipulating PDF files.
from reportlab.lib.units import inch
from datetime import datetime
from bson import ObjectId

from db.collections.OrdersCollection import OrdersCollection
from config.Static import Static
from window.Alert import Alert

class Invoices:
    def __init__(self, db, order_id):
        self._db_ = db
        self.order_id = order_id

        self._static_ = Static()

        self.init_model()

    def init_model(self):
        _collection_ = OrdersCollection(self._db_) #underscore indicates that the variable is intended for internal use within the class 
        self.order_data = _collection_.read_one({"_id": ObjectId(self.order_id)})

        if self.order_data:
            self.generate_invoice_pdf()
        else:
            Alert("error", f"This invoice {self.order_id} not found, try again")

    def generate_invoice_pdf(self):
        # Get the Downloads folder path based on the operating system
        downloads_folder = str(Path.home() / "Downloads")
        now = datetime.now()
        creation_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        pdf_file = os.path.join(downloads_folder, f"invoice-{creation_date}.pdf")

        # Create a PDF canvas
        pdf = canvas.Canvas(pdf_file, pagesize=A4)

        company_info = self._static_.get("company_info")
        products = self.order_data["products"]

        path = os.getcwd()
        path_imgs = os.path.join(path, "src/images")
        path_logo = os.path.join(path_imgs, "logo.png")

        # Set company logo if exists
        if path_logo:
            pdf.drawImage(path_logo, 40, 740, width=1.5*inch, height=1.5*inch)

        # Add Invoice
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(400, 800, "INVOICE")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(400, 780, f"N°: {self.order_data['_id']}")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(400, 760, f'Creation date: {now.strftime("%Y/%m/%d %H:%M:%S")}')

        # Add company details
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 720, f"{company_info['name']}")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, 705, f"Address: {company_info['address']}")
        pdf.drawString(40, 690, f"Phone number: {company_info['phone_number']}")
        pdf.drawString(40, 675, f"Stadt: {company_info['stadt']}")

        # Add customer details
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, 650, "Invoice To:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(40, 635, f"Fullame: {self.order_data['first_name']} {self.order_data['last_name']}")
        pdf.drawString(40, 620, f"Email: {self.order_data['email']}")
        pdf.drawString(40, 605, f"Phone number: {self.order_data['phone_number']}")
        pdf.drawString(40, 590, f"City: {self.order_data['city']}")
        pdf.drawString(40, 575, f"Country: {self.order_data['country']}")

        # Add product table header
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(40, 540, "Product Name")
        pdf.drawString(220, 540, "Price")
        pdf.drawString(300, 540, "Quantity")
        pdf.drawString(380, 540, "Total")

        # Add product items
        y = 525
        pdf.setFont("Helvetica", 10)
        for product in products:
            pdf.drawString(40, y, product["product_name"])
            pdf.drawString(220, y, f"${float(product['price']):.2f}")
            pdf.drawString(300, y, str(product["quantity"]))
            pdf.drawString(380, y, f"${float(product['total']):.2f}")
            y -= 15

        # Add totals
        y -= 20
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(300, y, "Subtotal:")
        pdf.drawString(380, y, f"${float(self.order_data['subtotal'].replace('$', '')):.2f}")
        
        y -= 15
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(300, y, "Discount:")
        pdf.drawString(380, y, f"-${float(self.order_data['discount'].replace('$', '').replace('%', '')):.2f}")


        y -= 15
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(300, y, "Shipping Fee:")
        pdf.drawString(380, y, f"${float(self.order_data['shipping_fee'].replace('$', '')):.2f}")

        y -= 15
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(300, y, "Mehrwertsteuer:")
        pdf.drawString(380, y, f"${float(self.order_data['vat'].replace('$', '')):.2f}")

        y -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(300, y, "Total:")
        pdf.drawString(380, y, f"${float(self.order_data['total'].replace('$', '')):.2f}")

        # Save the PDF file in the Downloads folder
        pdf.save()

        Alert("success", f"Invoice saved as {pdf_file}")