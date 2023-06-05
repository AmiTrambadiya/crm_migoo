// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Done By Employee"] = {
	"filters": [
		{
			"fieldname": "period",
			"label": __("Period"),
			"fieldtype": "Select",
			"options": "Today\nYesterday\nLast 15 Days\nLast Month\nLast 3 Months\nLast 6 Months\nLast Year\nSelect Date Range",
			"default": "Today",
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"depends_on": "eval: doc.period=='Select Date Range' ",
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"depends_on": "eval: doc.period=='Select Date Range' ",
		},
	],
};
