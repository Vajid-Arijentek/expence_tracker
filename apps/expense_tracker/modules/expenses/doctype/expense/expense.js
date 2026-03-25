// Expense Client Script
frappe.ui.form.on('Expense', {
	refresh: function(frm) {
		// Add custom buttons
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button('Mark as Approved', function() {
				frappe.call({
					method: 'expense_tracker.api.mark_approved',
					args: {
						expense: frm.doc.name
					},
					callback: function(r) {
						frm.reload_doc();
					}
				});
			}, 'Status');
		}

		// Show total expenses for the month
		if (frm.doc.expense_date) {
			frappe.call({
				method: 'expense_tracker.api.get_monthly_total',
				args: {
					date: frm.doc.expense_date
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(__('Monthly Total: {0}', [r.message]), 'blue');
					}
				}
			});
		}
	},

	receipt_attached: function(frm) {
		// Toggle receipt image field visibility
		frm.toggle_reqd('receipt_image', frm.doc.receipt_attached);
	},

	amount: function(frm) {
		// Calculate and show category-wise total
		if (frm.doc.expense_category && frm.doc.amount) {
			frappe.call({
				method: 'expense_tracker.api.get_category_total',
				args: {
					category: frm.doc.expense_category
				},
				callback: function(r) {
					if (r.message) {
						frm.dashboard.add_indicator(
							__('Category Total: {0}', [format_currency(r.message)]),
							'green'
						);
					}
				}
			});
		}
	}
});
