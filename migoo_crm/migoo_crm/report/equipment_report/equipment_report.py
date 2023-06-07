# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "name",
            "width": 200,
        },
        {
            "label": _("Equipment Main Category"),
            "fieldname": "item_group",
            "width": 200,
        },
        {
            "label": _("Equipment Sub Category"),
            "fieldname": "equipment_main_category",
            "width": 200,
        },
        {
            "label": _("Supplier"),
            "fieldname": "supplier_name",
            "width": 200,
        },
        {
            "label": _("RTO Registration"),
            "fieldname": "rto_register",
            "width": 180,
        },
        {
            "label": _("Equipment Verify"),
            "fieldname": "equipment_verify",
            "width": 200,
        },


    ]

    data = []
    query = """
		select
    		name,
    		item_group,
    		equipment_main_category,
    		supplier_name,
    		rto_register,
    		equipment_verify
		from
    		`tabItem`
    	"""

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += "where DATE(creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
