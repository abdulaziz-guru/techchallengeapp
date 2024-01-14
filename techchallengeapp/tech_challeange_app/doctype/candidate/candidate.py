# Copyright (c) 2024, Osman and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document


class Candidate(Document):

	def validate(self):
		self.validate_email()
		self.validate_status()

	def before_insert(self):
		self.validate_unique_name_email()

	def validate_email(self):
		pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
		if not re.match(pattern, self.email):
			frappe.throw("Invalid Email")

	def validate_status(self):
		status_field = frappe.get_meta("Candidate").get_field("status")
		if self.status not in status_field.options.split("\n"):
			frappe.throw("Invalid Status")

	def validate_unique_name_email(self):
		if frappe.db.exists({"doctype": "Candidate", "name": self.name}):
			frappe.throw("Candidate Name already exists")
		elif frappe.db.exists({"doctype": "Candidate", "email": self.email}):
			frappe.throw("Candidate Email already exists")
		elif frappe.db.exists({"doctype": "Candidate", "name": self.name, "email": self.email}):
			frappe.throw("Candidate already exists")
