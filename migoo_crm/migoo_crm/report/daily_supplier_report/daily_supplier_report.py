# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist(allow_guest=1)
def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "supplier_name",
            "width": 200,
        },
        {
            "label": _("Company Name"),
            "fieldname": "company_name",
            "width": 250,
        },
        {
            "label": _("Mobile No"),
            "fieldname": "mobile_number",
            "width": 200,
        },
        {
            "label": _("Email"),
            "fieldname": "email",
            "width": 250,
        },
        {
            "label": _("'Verified Or Not"),
            "fieldname": "verify",
            "width": 200,
        },



    ]

    data = []
    query = """
			select
    			supplier_name,
                verify,
                company_name,
                mobile_number,
				email
			from
    			`tabSupplier`
    """

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += "where DATE(creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
