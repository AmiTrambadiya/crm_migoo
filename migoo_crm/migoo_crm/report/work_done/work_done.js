// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Done"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},

		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
	]
};
