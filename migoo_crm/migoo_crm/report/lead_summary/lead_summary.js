// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Summary"] = {
	"filters": [
		{
			"fieldname": "creation",
			"label": __("Period"),
			"fieldtype": "Select",
			"options": "Daily\nTill Date\nDo Not Contact\nTotal",
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			'depends_on': 'eval:doc.creation === "Till Date"',

		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			'depends_on': 'eval:doc.creation === "Till Date"',
		}
	]
};
