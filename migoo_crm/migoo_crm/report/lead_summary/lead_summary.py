# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime


@frappe.whitelist()
def execute(filters=None):
    columns = [{
        "label": _("Name"),
        "fieldname": "lead_name",
        "width": 130,
    }]
    data = []

    # Check the value of the filter
    period = filters.get("creation")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    query = '''
    select lead_name
    from `tabLead`
    '''
    if period == "Daily":
        query += " WHERE DATE(creation) = CURDATE()"
    elif period == "Till Date":
        if from_date and to_date:
            query += f" WHERE DATE(creation) >= '{from_date}' AND DATE(creation) <= '{to_date}'"
        else:
            last_date = datetime.date.today() - datetime.timedelta(days=1)  # Get the last date
            query += f" WHERE DATE(creation) <= '{last_date}'"

    elif period == "Till Date":
        pass

    elif period == "Do Not Contact":
        query += " WHERE status='Do Not Contact'"

    data = frappe.db.sql(query, as_dict=1)

    return columns, data
