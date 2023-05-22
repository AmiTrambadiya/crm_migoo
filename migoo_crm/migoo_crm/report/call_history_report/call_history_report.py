# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {
            "label": _("Agent"),
            "fieldname": "agent_name",
            "width": 140,
        },
        {
            "label": _("Agent Number"),
            "fieldname": "agent_number",
            "width": 130,
        },
        {
            "label": _("Client Number"),
            "fieldname": "client_number",
            "width": 130,
        },
        {
            "label": _("Status Of call"),
            "fieldname": "status",
            "width": 130,
        },
        {
            "label": _("Call Duration (In Seconds)"),
            "fieldname": "call_duration",
            "width": 130,
        },
        {
            "label": _("Recording"),
            "fieldname": "recording_url",
            "width": 300,
        },
        {
            "label": _("Recoding"),
            "fieldname": "Recordings",
            "width": 150,
        },
    ]

    data = []
    query = """
        SELECT
            agent_name,
            agent_number,
            client_number,
            status,
            call_duration,
            recording_url,
            CONCAT('<a href="', cl.recording_url, '" class="btn pt-0 pb-0" style="background-color:#e6992a;color:#ffffff;">Open Recording</a>') AS 'Recordings'
        FROM
            `tabCall Logs` cl
            INNER JOIN `tabUser` u ON
            u.phone = cl.agent_number
    """

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += " WHERE DATE(cl.creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
