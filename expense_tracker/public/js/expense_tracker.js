/**
 * Expense Tracker - Common JavaScript Functions
 */

expense_tracker = {
	// Format currency for display
	format_currency: function(amount) {
		return format_currency(amount, frappe.boot.sysdefaults.currency);
	},

	// Show expense summary
	show_summary: function(date) {
		frappe.call({
			method: 'expense_tracker.api.get_daily_expenses',
			args: { date: date },
			callback: function(r) {
				if (r.message) {
					let total = 0;
					r.message.forEach(function(exp) {
						total += exp.amount;
					});
					frappe.msgprint(__("Total expenses for {0}: {1}", [date, expense_tracker.format_currency(total)]));
				}
			}
		});
	},

	// Quick add expense dialog
	quick_add_expense: function() {
		const dialog = new frappe.ui.Dialog({
			title: __('Quick Add Expense'),
			fields: [
				{fieldname: 'expense_date', fieldtype: 'Date', label: __('Date'), default: frappe.datetime.get_today()},
				{fieldname: 'expense_category', fieldtype: 'Link', label: __('Category'), options: 'Expense Category', reqd: 1},
				{fieldname: 'amount', fieldtype: 'Currency', label: __('Amount'), reqd: 1},
				{fieldname: 'description', fieldtype: 'Data', label: __('Description')},
				{fieldname: 'payment_method', fieldtype: 'Select', label: __('Payment Method'),
					options: 'Cash\nCredit Card\nDebit Card\nBank Transfer\nUPI\nDigital Wallet\nOther'}
			],
			primary_action: function() {
				const values = dialog.get_values();
				frappe.call({
					method: 'expense_tracker.api.expense_api.create_expense',
					args: { data: JSON.stringify(values) },
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__('Expense created successfully: {0}', [r.message.name]));
							dialog.hide();
							// Refresh current page if on expense list
							if (cur_list && cur_list.refresh) {
								cur_list.refresh();
							}
						}
					}
				});
			},
			primary_action_label: __('Add Expense')
		});
		dialog.show();
	}
};

// Add quick add button to expense list
$(document).on('app_ready', function() {
	if (frappe.route && frappe.route.doctype === 'Expense') {
		// Add any custom UI enhancements here
	}
});
