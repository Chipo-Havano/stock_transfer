// Copyright (c) 2024, Chipo Hameja and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cash Transfer", {
 	refresh(frm) {
		frm.set_query("source_debit_account", () => {
			return {
				filters: {
					company: frm.doc.source_company
				}
			}
		});
		frm.set_query("source_credit_account", () => {
			return {
				filters: {
					company: frm.doc.source_company
				}
			}
		});

		frm.set_query("target_debit_account", () => {
			return {
				filters: {
					company: frm.doc.target_company
				}
			}
		});
		frm.set_query("target_credit_account", () => {
			return {
				filters: {
					company: frm.doc.target_company
				}
			}
		});
 	},
});
