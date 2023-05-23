// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Summary"] = {
	"filters": [{
		"fieldname": "period",
		"label": __("Period"),
		"fieldtype": "Select",
		"options": "\nDaily\nWeekly\nMonthly",
		// "default": "Monthly",
		// "reqd": 1
	}]
};
