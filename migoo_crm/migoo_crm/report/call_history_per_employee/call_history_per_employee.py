# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Agent"),
            "fieldname": "agent_name",
            "width": 165,
        },
        {
            "label": _("Agent Number"),
            "fieldname": "agent_number",
            "width": 165,
        },
        {
            "label": _("Client Number"),
            "fieldname": "client_number",
            "width": 165,
        },
        {
            "label": _("Status Of call"),
            "fieldname": "status",
            "width": 150,
        },
        {
            "label": _("Call Duration (In Seconds)"),
            "fieldname": "call_duration",
            "width": 165,
        },
        {
            "label": _("DID Number"),
            "fieldname": "did_number",
            "width": 165,
        },
        {
            "label": _("Recoding"),
            "fieldname": "Recordings",
            "width": 165,
        },
    ]

    user = frappe.session.user

    data = []

    if 'System Manager' in frappe.get_roles(user):

        query = """
            SELECT
                agent_name,
                agent_number,
                client_number,
                cl.status,
                call_duration,
                did_number,
                CONCAT('<a href="', cl.recording_url, '" class="btn pt-0 pb-0" style="background-color:#e6992a;color:#ffffff;">Open Recording</a>') AS 'Recordings'
            FROM
                `tabCall Logs` cl
                INNER JOIN `tabUser` u ON u.phone = cl.agent_number
                INNER JOIN `tabEmployee` e ON e.user_id = u.name

        """

        if filters and filters.get("from_date") and filters.get("to_date"):
            query += " AND DATE(cl.creation) BETWEEN %s AND %s"
            query_params.extend(
                [filters.get("from_date"), filters.get("to_date")])

        data = frappe.db.sql(query, as_dict=1)

    else:

        employee = frappe.get_doc("Employee", {"user_id": user})

        query = """
            SELECT
                agent_name,
                agent_number,
                client_number,
                cl.status,
                call_duration,
                did_number,
                CONCAT('<a href="', cl.recording_url, '" class="btn pt-0 pb-0" style="background-color:#e6992a;color:#ffffff;">Open Recording</a>') AS 'Recordings'
            FROM
                `tabCall Logs` cl
                INNER JOIN `tabUser` u ON u.phone = cl.agent_number
                INNER JOIN `tabEmployee` e ON e.user_id = u.name

            where e.name= %s
        """

        query_params = [employee.name]

        if filters and filters.get("from_date") and filters.get("to_date"):
            query += " AND DATE(cl.creation) BETWEEN %s AND %s"
            query_params.extend(
                [filters.get("from_date"), filters.get("to_date")])

        data = frappe.db.sql(query, tuple(query_params), as_dict=1)

    return columns, data
