# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "lead_name",
            "width": 130,
        },
        {
            "label": _("Company Name"),
            "fieldname": "company_name",
            "width": 130,
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "width": 95,
        },
        {
            "label": _("Lead Type"),
            "fieldname": "type",
            "width": 110,
        },
        {
            "label": _("Email"),
            "fieldname": "email_id",
            "width": 130,
        },
        {
            "label": _("Mobile no"),
            "fieldname": "mobile_no",
            "width": 110,
        },
        {
            "label": _("City"),
            "fieldname": "city",
            "width": 110,
        },
        {
            "label": _("State"),
            "fieldname": "state",
            "width": 110,
        },
        {
            "label": _("Lead Owner"),
            "fieldname": "lead_owner",
            "width": 110,
        },
        {
            "label": _("Request Type"),
            "fieldname": "request_type",
            "width": 110,
        },
    ]

    data = []

    user = frappe.session.user

    query = """
    SELECT
        lead_name,
        company_name,
        l.status,
        type,
        email_id,
        l.mobile_no,
        city,
        state,
        lead_owner,
        rt.request_type
    FROM
        `tabLead` l
        RIGHT JOIN `tabEmployee` e ON e.user_id = l.lead_owner
        INNER JOIN `tabRequest Types` rt ON l.name = rt.parent
    WHERE
        rt.request_type = 'Spare Parts'

	"""
    query_params = {}

    if 'System Manager' not in frappe.get_roles(user):
        employee = frappe.get_doc("Employee", {"user_id": user})
        query += " AND l.lead_owner = %(lead_owner)s"
        query_params["lead_owner"] = employee.company_email

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += " AND DATE(l.creation) BETWEEN %(from_date)s AND %(to_date)s"
        query_params.update(filters)

    data = frappe.db.sql(query, query_params, as_dict=1)

    return columns, data
