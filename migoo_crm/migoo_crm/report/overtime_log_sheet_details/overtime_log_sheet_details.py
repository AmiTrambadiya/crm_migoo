# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist(allow_guest=1)
def execute(filters=None):
    columns = [
        {
            "label": _("Date"),
            "fieldname": "Date",
            "fieldtype": "Date",
        },
        {
            "label": _("Equipment"),
            "fieldname": "equipment",
            "fieldtype": "Link",
            "options": "Item",
        },
        {
            "label": _("Equipment Number"),
            "fieldname": "equipment_no",
        },
        {
            "label": _("Driver"),
            "fieldname": "Driver",
            "fieldtype": "Link",
            "options": "Driver",
        },
        {
            "label": _("Status"),
            "fieldname": "Status",
        },
        {
            "label": _("Start Time"),
            "fieldname": "StartTime",
        },
        {
            "label": _("End Time"),
            "fieldname": "EndTime",
        },
        {
            "label": _("Start KM"),
            "fieldname": "StartKM",
        },
        {
            "label": _("End KM"),
            "fieldname": "EndKM",
        },
        {
            "label": _("Total Working Time"),
            "fieldname": "TotalWorkingTime",
        },
        {
            "label": _("Total Ideal Time"),
            "fieldname": "TotalIdealTime",
        },
        {
            "label": _("Total Breakdown Time"),
            "fieldname": "TotalBreakdownTime",
        },
        {
            "label": _("Total Time"),
            "fieldname": "TotalTime",
        },
        {
            "label": _("Total Overtime"),
            "fieldname": "TotalOvertime",
        },
        {
            "label": _("Total Km"),
            "fieldname": "TotalKm",
        },
        {
            "label": _("Remarks"),
            "fieldname": "Remarks",
        },
        {
            "label": _("Supplier"),
            "fieldname": "Supplier",
            "fieldtype": "Link",
            "options": "Supplier",
        },
        {
            "label": _("Equipment Planning"),
            "fieldname": "EquipmentPlanning",
            "fieldtype": "Link",
            "options": "Resource Planning",
        },
    ]

    data = []

    query = """
    SELECT 
        l.date AS "Date",
        l.driver AS "Driver",
        w.status AS "Status",
        w.start_time AS "StartTime",
        w.end_time AS "EndTime",
        w.start_km AS "StartKM",
        w.end_km AS "EndKM",
        l.total_working_time AS "TotalWorkingTime",
        l.total_ideal_time AS "TotalIdealTime",
        l.total_breckdown_time AS "TotalBreakdownTime",
        l.total_time AS "TotalTime",
        overtime_calculation AS "TotalOvertime",
        l.total_km AS "TotalKm",
        w.remarks AS "Remarks",
        l.supplier AS "Supplier",
        equipment,
        equipment_no,
        l.resource_planning AS "EquipmentPlanning"
        
    FROM 
        `tabLog Sheet` AS l
    LEFT JOIN `tabWorking Details` w
        ON w.parent = l.name
        
    WHERE overtime_calculation != 0
    """

    query_params = {}

    if filters.get("from_date") and filters.get("to_date"):
        if "WHERE" in query:
            query += "AND l.creation BETWEEN %(from_date)s AND %(to_date)s"
        else:
            query += "WHERE l.creation BETWEEN %(from_date)s AND %(to_date)s"
        query_params.update(filters)

    if filters.get("equipment"):
        if "WHERE" in query:
            query += " AND l.equipment = %(equipment)s"
        else:
            query += " WHERE l.equipment = %(equipment)s"
        query_params.update(filters)

    if filters.get("logsheet"):
        if "WHERE" in query:
            query += " AND l.name = %(logsheet)s"
        else:
            query += " WHERE l.name = %(logsheet)s"
        query_params.update(filters)

    if filters.get("resource_planning"):
        if "WHERE" in query:
            query += " AND l.resource_planning = %(resource_planning)s"
        else:
            query += " WHERE l.resource_planning = %(resource_planning)s"
        query_params.update(filters)

    if filters.get("supplier"):
        if "WHERE" in query:
            query += " AND l.supplier = %(supplier)s"
        else:
            query += " WHERE l.supplier = %(supplier)s"
        query_params.update(filters)

    if filters.get("customer"):
        if "WHERE" in query:
            query += " AND l.customer = %(customer)s"
        else:
            query += " WHERE l.customer = %(customer)s"
        query_params.update(filters)

    if filters.get("driver"):
        if "WHERE" in query:
            query += " AND l.driver = %(driver)s"
        else:
            query += " WHERE l.driver = %(driver)s"
        query_params.update(filters)

    if filters.get("status"):
        if "WHERE" in query:
            query += " AND status = %(status)s"
        else:
            query += " WHERE status = %(status)s"
        query_params.update(filters)

    data = frappe.db.sql(query, query_params, as_dict=1)
    return columns, data
