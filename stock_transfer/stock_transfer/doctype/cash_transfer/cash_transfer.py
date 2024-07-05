# Copyright (c) 2024, Chipo Hameja and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class CashTransfer(Document):
	def before_submit(self):
		self.create_journal_entry(self.source_company, self.source_debit_account, self.source_credit_account)
		self.create_journal_entry(self.target_company, self.target_debit_account, self.target_credit_account, False)

		self.status = "Complete"

	def create_journal_entry(self, company, debit_account, credit_account, source=True):
		new_je = frappe.get_doc({
			"doctype": "Journal Entry",
			"company": company,
			"posting_date": today()
		})

		new_je.append("accounts", {
			"account": credit_account,
			"credit_in_account_currency": self.amount
		})

		new_je.append("accounts", {
			"account": debit_account,
			"debit_in_account_currency": self.amount
		})

		new_je.insert().submit()

		if source:
			self.source_journal_entry = new_je.name
		else:
			self.target_journal_entry = new_je.name

