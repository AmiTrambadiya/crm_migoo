# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "supplier_name",
            "width": 250,
        },
        {
            "label": _("Company Name"),
            "fieldname": "company_name",
            "width": 250,
        },
        {
            "label": _("Mobile No"),
            "fieldname": "mobile_number",
            "width": 220,
        },
        {
            "label": _("Email"),
            "fieldname": "email",
            "width": 250,
        },
        {
            "label": _("Verified Or Not"),
            "fieldname": "verify",
            "width": 180,
        },

    ]

    data = []

    user = frappe.session.user

    query = """
    select
    	supplier_name,
        company_name,
    	verify,
    	company_name,
    	mobile_number,
    	email
	from
    	`tabSupplier`

	"""
    query_params = {}

    if 'System Manager' not in frappe.get_roles(user):
        employee = frappe.get_doc("Employee", {"user_id": user})
        query += " WHERE owner_name = %(owner_name)s"
        query_params["owner_name"] = employee.company_email

    if filters and filters.get("from_date") and filters.get("to_date"):
        if 'System Manager' not in frappe.get_roles(user):
            query += " AND"
        else:
            query += " WHERE"
            query += " DATE(creation) BETWEEN %(from_date)s AND %(to_date)s"
            query_params.update(filters)

    data = frappe.db.sql(query, query_params, as_dict=1)

    return columns, data
