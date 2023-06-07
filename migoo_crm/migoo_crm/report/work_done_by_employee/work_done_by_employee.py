import frappe
from frappe import _
from datetime import datetime, timedelta


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "name",
            "width": 170,
            "fieldtype": "Data",
        },
        {
            "label": _("Equipment"),
            "fieldname": "Equipment",
            "width": 120,
        },
        {
            "label": _("Supplier"),
            "fieldname": "Supplier",
            "width": 120,
        },
        {
            "label": _("Customer"),
            "fieldname": "Customer",
            "width": 120,
        },
        {
            "label": _("User"),
            "fieldname": "User",
            "width": 120,
        },
        {
            "label": _("Call Logs"),
            "fieldname": "CallLogs",
            "width": 120,
        },
        {
            "label": _("Lead"),
            "fieldname": "Lead",
            "width": 120,
        },
        {
            "label": _("Opportunity"),
            "fieldname": "Opportunity",
            "width": 120,
        },
        {
            "label": _("Quotation"),
            "fieldname": "Quotation",
            "width": 120,
        },
    ]

    data = []
    query = """
        SELECT
            u.full_name AS 'name',
            u.phone AS 'phone',
            (
                SELECT
                    COUNT(*)
                FROM
                    `tabItem`
                WHERE
                    owner = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "Equipment",

            (
                SELECT
                    COUNT(*)
                FROM
                    `tabSupplier`
                WHERE
                    owner_name = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "Supplier",

            (
                SELECT
                    COUNT(*)
                FROM
                    `tabCustomer`
                WHERE
                    owner = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "Customer",

            (
                SELECT
                    COUNT(*)
                FROM
                    `tabUser`
                WHERE
                    owner = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "User",

            (
                SELECT
                    COUNT(*)
                FROM
                    `tabCall Logs`
                WHERE
                    agent_number = u.phone
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "CallLogs",

            (
                SELECT
                    COUNT(*)
                FROM
                    `tabLead`
                WHERE
                    lead_owner = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "Lead",

            (
                SELECT
                    COUNT(*)
                FROM
                    `tabOpportunity`
                WHERE
                    opportunity_owner = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "Opportunity",
            (
                SELECT
                    COUNT(*)
                FROM
                    `tabQuotation`
                WHERE
                    owner = u.name
                    AND DATE(creation) BETWEEN %(start_date)s AND %(end_date)s
            ) AS "Quotation"
        FROM
            `tabUser` u
        WHERE
            u.module_profile = "Sales Team"
            AND enabled = 1
    """

    values = {
        "start_date": None,
        "end_date": None
    }

    if filters and filters.get("period") == "Today":
        today = datetime.now().strftime("%Y-%m-%d")
        values["start_date"] = today
        values["end_date"] = today

    elif filters and filters.get("period") == "Yesterday":
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        values["start_date"] = yesterday
        values["end_date"] = yesterday

    elif filters and filters.get("period") == "Last 15 Days":
        start_date = datetime.now() - timedelta(days=14)
        values["start_date"] = start_date.strftime("%Y-%m-%d")
        values["end_date"] = datetime.now().strftime("%Y-%m-%d")

    elif filters and filters.get("period") == "Last Month":
        start_date = datetime.now() - timedelta(days=30)
        values["start_date"] = start_date.strftime("%Y-%m-%d")
        values["end_date"] = datetime.now().strftime("%Y-%m-%d")

    elif filters and filters.get("period") == "Last 3 Months":
        start_date = datetime.now() - timedelta(days=89)
        values["start_date"] = start_date.strftime("%Y-%m-%d")
        values["end_date"] = datetime.now().strftime("%Y-%m-%d")

    elif filters and filters.get("period") == "Last 6 Months":
        start_date = datetime.now() - timedelta(days=179)
        values["start_date"] = start_date.strftime("%Y-%m-%d")
        values["end_date"] = datetime.now().strftime("%Y-%m-%d")

    elif filters and filters.get("period") == "Last Year":
        start_date = datetime.now() - timedelta(days=365)
        values["start_date"] = start_date.strftime("%Y-%m-%d")
        values["end_date"] = datetime.now().strftime("%Y-%m-%d")

    elif filters and filters.get("period") == "Select Date Range":
        if filters.get("from_date") and filters.get("to_date"):
            values["start_date"] = filters["from_date"]
            values["end_date"] = filters["to_date"]
        else:
            start_date = datetime.now() - timedelta(days=30)
            values["start_date"] = start_date.strftime("%Y-%m-%d")
            values["end_date"] = datetime.now().strftime("%Y-%m-%d")

    data = frappe.db.sql(query, as_dict=1, values=values)
    return columns, data
