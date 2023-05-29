// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier and Equipment Report"] = {
	"filters": [
		{
			"fieldname": "suppliernames",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options":"Supplier",
		}
	]
};
