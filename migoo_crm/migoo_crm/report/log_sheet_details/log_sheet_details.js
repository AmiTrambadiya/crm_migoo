// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Log Sheet Details"] = {
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
		{
			"fieldname": "equipment",
			"label": __("Equipment"),
			"fieldtype": "Link",
			"options":"Item",
		},
		{
			"fieldname": "resource_planning",
			"label": __("Resource Planning"),
			"fieldtype": "Link",
			"options":"Resource Planning",
		},
		{
			"fieldname": "logsheet",
			"label": __("Log Sheet"),
			"fieldtype": "Link",
			"options":"Log Sheet",
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
			"fieldname": "driver",
			"label": __("Driver"),
			"fieldtype": "Link",
			"options":"Driver",
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options":"\nWorking\nIdeal\nBreakdown",
		},
	]
};
