# Copyright (c) 2023, vivek and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VendorList(Document):
	def before_save(self):
		aadhar_list = frappe.get_all('Vender List', filters={'aadhaar_number': self.aadhaar_number, 'name': ['!=', self.name]},fields ={'name','supplier_name'})
		if aadhar_list:
			frappe.throw(f"Aadhar number must be unique aadhar Exist for vendor '{aadhar_list[0].supplier_name}'")

		exist_supp=frappe.get_all("Supplier",filters={"name":self.name})
		if(not exist_supp):
			doc=frappe.new_doc("Supplier")
			doc.supplier_type=self.supplier_type
			doc.supplier_group=self.vendor_group
			doc.supplier_name=self.name1
			doc.branch=self.branch
			doc.insert()
			self.supplier_doc=doc.name
			doc.save()
			frappe.db.set_value("Supplier",str(self.supplier_doc),"name",self.name)
		
			cust=frappe.new_doc("Customer")
			cust.customer_type=self.supplier_type
			cust.customer_group=self.vendor_group
			cust.customer_name=self.name1
			cust.branch=self.branch
			cust.territory="India"
			cust.insert()
			self.customer_doc=cust.name
			cust.save()
			frappe.db.set_value("Customer",str(self.customer_doc),"name",self.name)

	def on_trash(self):
		frappe.delete_doc("Supplier",self.name)
		frappe.delete_doc("Customer",self.name)
	
