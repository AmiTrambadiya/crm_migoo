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
            # "width": 195,
        },
        {
            "label": _("Equipment Planning"),
            "fieldname": "resource_planning",
            # "width": 195,
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            # "width": 195,
        },
        {
            "label": _("Equipment Category"),
            "fieldname": "equipment_category",
            # "width": 170,
        },
        {
            "label": _("Agreement"),
            "fieldname": "agreement",
            # "width": 195,
        },
        {
            "label": _("Total Fuel"),
            "fieldname": "total_fuel",
            # "width": 195,
        },
        {
            "label": _("Supplier"),
            "fieldname": "supplier",
            # "width": 195,
        },
        {
            "label": _("Supplier Approve"),
            "fieldname": "supplier_approve",
            # "width": 195,
        },

    ]

    data = []

    user = frappe.session.user

    query = """
    SELECT
        name as "Name",
        resource_planning,
        customer,
    	equipment_category,
    	agreement,
    	total_fuel,
        supplier,
        supplier_approve
	FROM
   		`tabSummary Sheet`
	"""

    if filters and filters.get("start_date") and filters.get("end_date"):
        query += "where DATE(creation) BETWEEN %(start_date)s AND %(end_date)s"
    if filters.get("supplier"):
        query += "and supplier = %(supplier)s"
    if filters.get("customer"):
        query += "and customer = %(customer)s"
    if filters.get("agreement"):
        query += "and agreement = %(agreement)s"
            

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
