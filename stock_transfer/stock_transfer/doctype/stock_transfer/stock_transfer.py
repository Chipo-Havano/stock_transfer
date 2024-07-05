# Copyright (c) 2024, Chipo Hameja and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import frappe
from frappe import _

class StockTransfer(Document):
	def before_submit(self):
		self.create_stock_entry("Material Issue", self.source_company, self.s_warehouse, "")
		self.create_stock_entry("Material Receipt", self.target_company, "", self.t_warehouse)

		self.status = "Complete"

	def create_stock_entry(self, stock_entry_type, company, from_warehouse, to_warehouse):
		new_mt = frappe.get_doc({
			"doctype": "Stock Entry",
			"company": company,
			"stock_entry_type": stock_entry_type,
			"company": company,
			"from_warehouse": from_warehouse,
			"to_warehouse": to_warehouse,
		})

		for item in self.items:
			new_mt.append("items", {
				"item_code": item.item_code,
				"qty": item.qty,
				"rate": item.rate
			})

		new_mt.insert().submit()

		if stock_entry_type == "Material Issue":
			self.s_stock_entry = new_mt.name
		else:
			self.t_stock_entry = new_mt.name

	@frappe.whitelist()
	def get_item_price(self, item_code):
		price_exists = frappe.db.exists("Item Price", {"item_code": item_code, "buying": 1})

		if price_exists:
			item_price = frappe.db.get_value("Item Price", price_exists, "price_list_rate")

			return {"rate": item_price}

		else:
			return {"rate": 0.00}
