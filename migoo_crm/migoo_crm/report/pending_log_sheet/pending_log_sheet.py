# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": "100"
        },
        {
            "label": _("Equipment"),
            "fieldname": "equipment_sub_category",
            "fieldtype": "Data",
            "width": "170",
        },
        {
            "label": _("Equipment No"),
            "fieldname": "equipment_no",
            "fieldtype": "Data",
            "width": "170",
        },

        {
            "label": _("Supplier"),
            "fieldname": "name_of_suppier",
            "fieldtype": "Data",
            "options": "Supplier",
            "width": "170",
        },
        {
            "label": _("Driver"),
            "fieldname": "driver_name",
            "fieldtype": "Data",
            "width": "170",
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": "170",
        },
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Equipment Planning",
            "width": "170",
        },
    ]

    data = []

    query = """
		SELECT
			subquery.name,
			subquery.equipment_sub_category,
			subquery.supplier,
			subquery.equipment_no,
			subquery.name_of_suppier,
			subquery.email,
			subquery.driver_name,
			subquery.customer,
            driver,
			subquery.date
		FROM
			(
			SELECT
				`tabEquipment Planning`.name,
				`tabEquipment Planning`.equipment_sub_category,
				`tabEquipment Planning`.supplier,
				`tabEquipment Planning`.equipment_no,
				`tabSupplier`.name_of_suppier,
				`tabSupplier`.email,
				`tabEquipment Planning`.driver_name,
                `tabEquipment Planning`.driver,
				`tabEquipment Planning`.customer,
				DATE_ADD(`tabEquipment Planning`.start_date, INTERVAL seq.seq DAY) AS date
			FROM
				(
				SELECT
					(t4.num * 1000 + t3.num * 100 + t2.num * 10 + t1.num) AS seq
				FROM
					(SELECT 0 AS num UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t1,
					(SELECT 0 AS num UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t2,
					(SELECT 0 AS num UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t3,
					(SELECT 0 AS num UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) AS t4
				ORDER BY seq
				) AS seq
			JOIN `tabEquipment Planning` ON seq.seq <= DATEDIFF(`tabEquipment Planning`.end_date, `tabEquipment Planning`.start_date)
			JOIN `tabSupplier` ON `tabEquipment Planning`.supplier = `tabSupplier`.name
			LEFT JOIN `tabLog Sheet` ON DATE(`tabLog Sheet`.date) = DATE_ADD(`tabEquipment Planning`.start_date, INTERVAL seq.seq DAY)
				AND `tabEquipment Planning`.name = `tabLog Sheet`.resource_planning
                 WHERE
            `tabLog Sheet`.date IS NULL
			) AS subquery
           
            WHERE
    		subquery.date < CURDATE()
		"""

    query_params = {}

    if filters.get("from_date") and filters.get("to_date"):
        if "WHERE" in query:
            query += "AND date BETWEEN %(from_date)s AND %(to_date)s"
        else:
            query += "WHERE date BETWEEN %(from_date)s AND %(to_date)s"
        query_params.update(filters)

    if filters.get("name"):
        if "WHERE" in query:
            query += " AND name = %(name)s"
        else:
            query += " WHERE name = %(name)s"
        query_params.update(filters)

    if filters.get("supplier"):
        if "WHERE" in query:
            query += " AND subquery.supplier = %(supplier)s"
        else:
            query += " WHERE subquery.supplier = %(supplier)s"
        query_params.update(filters)

    if filters.get("driver"):
        if "WHERE" in query:
            query += " AND subquery.driver = %(driver)s"
        else:
            query += " WHERE subquery.driver = %(driver)s"
        query_params.update(filters)

    if filters.get("customer"):
        if "WHERE" in query:
            query += " AND subquery.customer = %(driver)s"
        else:
            query += " WHERE subquery.customer = %(driver)s"
        query_params.update(filters)

    if filters.get("equipment_sub_category"):
        if "WHERE" in query:
            query += " AND subquery.equipment_sub_category = %(equipment_sub_category)s"
        else:
            query += " WHERE subquery.equipment_sub_category = %(equipment_sub_category)s"
        query_params.update(filters)

    query += " ORDER BY subquery.date desc"

    data = frappe.db.sql(query, query_params, as_dict=True)
    return columns, data