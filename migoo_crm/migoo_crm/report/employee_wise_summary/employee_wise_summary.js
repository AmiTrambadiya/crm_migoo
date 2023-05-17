// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Wise Summary"] = {
	"filters": [{
		"fieldname": "period",
		"label": __("Period"),
		"fieldtype": "Select",
		"options": "\nDaily\nWeekly\nMonthly",
		"default": "Daily",
		"reqd": 1
	},
	{
			"fieldname": "user",
			"label": __("User"),
			"fieldtype": "Link",
			"options": "User",
			"default":""
	}
	]
};
