// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Equipment Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},
	]
};