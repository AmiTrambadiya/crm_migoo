# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "Name",
            "width": 200,
        },
        {
            "label": _("Equipment Main Category"),
            "fieldname": "EquipmentMainCategory",
            "width": 200,
        },
        {
            "label": _("Equipment Sub Category"),
            "fieldname": "EquipmentSubCategory",
            "width": 200,
        },
        {
            "label": _("Supplier"),
            "fieldname": "Supplier",
            "width": 200,
        },
        {
            "label": _("RTO Registration"),
            "fieldname": "RTORegistration",
            "width": 200,
        },
        {
            "label": _("Equipment Verify"),
            "fieldname": "EquipmentVerify",
            "width": 100,
        },

    ]

    data = []
    query = """
			select
    			name as 'Name',
    			item_group as 'EquipmentMainCategory',
    			equipment_main_category as 'EquipmentSubCategory',
    			supplier_name as 'Supplier',
    			rto_register as 'RTORegistration',
    			equipment_verify as 'EquipmentVerify'
			from
    			`tabItem`
    """

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += "where DATE(creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
