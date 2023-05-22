# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "name",
            "width": 170,
            "fieldtype": "Data",
        },
        {
            "label": _("Phone No"),
            "fieldname": "phone",
            "width": 130,
        },
        {
            "label": _("Equipment"),
            "fieldname": "Equipment",
            "width": 140,
        },

        {
            "label": _("Supplier"),
            "fieldname": "Supplier",
            "width": 140,
        },
        {
            "label": _("Call Logs"),
            "fieldname": "CallLogs",
            "width": 140,
        },
        {
            "label": _("Lead"),
            "fieldname": "Lead",
            "width": 140,
        },
        {
            "label": _("Opportunity"),
            "fieldname": "Opportunity",
            "width": 140,
        },
        {
            "label": _("Quotation"),
            "fieldname": "Quotation",
            "width": 140,
        },
    ]

    data = []
    query = """
       	SELECT
    		u.name as 'name',
    		u.phone as 'phone',
    	(
    	    SELECT
    	        COUNT(*)
    	    FROM
    	        `tabItem`
    	    WHERE
    	        owner = u.name
    	) AS "Equipment",
    	(
    	    SELECT
    	        COUNT(*)
    	    FROM
    	        `tabSupplier`
    	    WHERE
    	        owner_name = u.name
    	) AS "Supplier",
    	(
    	    SELECT
    	        COUNT(*)
    	    FROM
    	        `tabCall Logs`
    	    WHERE
    	        agent_number = u.phone
    	) AS "CallLogs",
    	(
    	    SELECT
    	        COUNT(*)
    	    FROM
    	        `tabLead`
    	    WHERE
    	        lead_owner = u.name
    	) AS "Lead",
    	(
    	    SELECT
    	        COUNT(*)
    	    FROM
    	        `tabOpportunity`
    	    WHERE
    	        opportunity_owner = u.name
    	) AS "Opportunity",
    	(
    	    SELECT
    	        COUNT(*)
    	    FROM
    	        `tabQuotation`
    	    WHERE
    	        owner = u.name
    	) AS "Quotation"
	FROM
    	`tabUser` u
	WHERE
    	u.module_profile = "Sales Team"
	GROUP BY
    	u.name
    """

    # if filters and filters.get("from_date") and filters.get("to_date"):
    #     query += " WHERE DATE(cl.creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
