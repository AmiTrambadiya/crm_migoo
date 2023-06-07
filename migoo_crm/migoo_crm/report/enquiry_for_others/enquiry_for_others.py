# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "Name",
            "width": 195,
        },
        {
            "label": _("Company"),
            "fieldname": "company_name",
            "width": 195,
        },
        {
            "label": _("Email"),
            "fieldname": "email_address",
            "width": 195,
        },
        {
            "label": _("Mobile No"),
            "fieldname": "mobile_no",
            "width": 170,
        },
        {
            "label": _("Equipment Details"),
            "fieldname": "item_details",
            "width": 195,
        },
        {
            "label": _("Inquiry Source"),
            "fieldname": "inquiry_source",
            "width": 195,
        },

    ]

    data = []

    user = frappe.session.user

    query = """
    SELECT
        concat(`first_name`, ' ', `last_name`) as "Name",
        company_name,
        email_address,
    	mobile_no,
    	item_details,
    	inquiry_source
	FROM
   		`tabInquiry Form`
	WHERE
    	request = 'Others'
	"""

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += "AND DATE(creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
