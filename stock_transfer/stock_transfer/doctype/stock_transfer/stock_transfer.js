// Copyright (c) 2024, Chipo Hameja and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Transfer", {
	refresh(frm) {
		frm.set_query('t_warehouse', () => {
			return {
				filters: {
					company: frm.doc.target_company
				}
			}
		});

		frm.set_query('s_warehouse', () => {
			return {
				filters: {
					company: frm.doc.source_company
				}
			}
		});
	},
	calculate_amount: function(frm) {
		let total = 0.00;

		const { items } = frm.doc;

		$.each(items, function(i){
			total += items[i].amount;
		});

		frm.set_value("total", total);
	}
});

frappe.ui.form.on("Stock Transfer Detail", {
	item_code: function(frm, cdt, cdn) {
		const ct = locals[cdt][cdn];

		const args = {
			"item_code": ct.item_code
		}

		frappe.call({
			doc: frm.doc,
			method: "get_item_price",
			args: args,
			callback: function (r) {
				if (r.message) {
					console.log(r.message);

					$.each(r.message, function (k, v) {
						if (v) {
							console.log(`K: ${k} V: ${v}`)
							frappe.model.set_value(cdt, cdn, k, v); // qty and it's subsequent fields weren't triggered
							frappe.model.set_value(cdt, cdn, "amount", v * ct.qty)
						}
					});
					refresh_field("items");

					console.log("Triggering")

					frm.trigger("calculate_amount")
				}
			}
		})
	},

	qty: function(frm, cdt, cdn) {
		const ct  = locals[cdt][cdn];

		frappe.model.set_value(cdt, cdn, "amount", ct.rate * ct.qty);

		frm.trigger("calculate_amount");
	}
});