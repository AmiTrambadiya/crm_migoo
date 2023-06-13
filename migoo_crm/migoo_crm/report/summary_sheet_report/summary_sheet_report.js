// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Summary Sheet report"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "end_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options":"Supplier",
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options":"Customer",
		},
		{
			"fieldname": "agreement",
			"label": __("Agreement"),
			"fieldtype": "Link",
			"options":"Sales Order",
		}
	]
};
