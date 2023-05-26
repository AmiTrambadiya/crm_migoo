# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist(allow_guest=1)
def execute(filters=None):
    columns = [
        {
            "label": _("Item Group"),
            "fieldname": "item_group_name",
            "width": 239,
        },
        {
            "label": _("Total"),
            "fieldname": "Total",
            "width": 180,
        },
        {
            "label": _("Working"),
            "fieldname": "Working",
            "width": 180,
        },
        {
            "label": _("Ideal"),
            "fieldname": "Ideal",
            "width": 180,
        },
        {
            "label": _("BreakDown"),
            "fieldname": "BreakDown",
            "width": 180,
        },
        {
            "label": _("Free"),
            "fieldname": "Free",
            "width": 180,
        },
    ]

    user = frappe.session.user

    data = []

    if 'System Manager' in frappe.get_roles(user):

        query = """
            WITH working as(
       select
              supplier,
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Working'
       group by
              item_group,
               equipment_status
),
ideal as(
       select
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Ideal'
       group by
              item_group
),
breakdown as(
       select
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Breakdown'
       group by
              item_group
),
occupied as(
       select
              item_group,
         equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Occupied With Migoo'
       group by
              item_group
),
free as(
       select
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Free'
       group by
              item_group
)
select
       ig.item_group_name,
       count(i.item_group) as 'Total',
       count(working.equipment_status) as 'Working',
       count(ideal.equipment_status) as 'Ideal',
       count(breakdown.equipment_status) as 'BreakDown',
       count(free.equipment_status) as 'Free',
        i.supplier as 'S:Link/Supplier:-10'
from
       `tabItem Group` ig
       left outer JOIN `tabItem` i ON i.item_group = ig.item_group_name
       left outer JOIN working on ig.item_group_name = working.item_group
       and working.equipment_status = i.equipment_status
       left outer JOIN ideal on ig.item_group_name = ideal.item_group
       and ideal.equipment_status = i.equipment_status
       left outer JOIN breakdown on ig.item_group_name = breakdown.item_group
       and breakdown.equipment_status = i.equipment_status

       left outer JOIN free on ig.item_group_name = free.item_group
       and free.equipment_status = i.equipment_status
where
       ig.parent_item_group = 'All Equipment Groups'

group by
       ig.item_group_name
        """

        # if filters and filters.get("from_date") and filters.get("to_date"):
        #     query += " AND DATE(cl.creation) BETWEEN %s AND %s"
        #     query_params.extend(
        #         [filters.get("from_date"), filters.get("to_date")])

        data = frappe.db.sql(query, as_dict=1)

    else:

        supplier = frappe.get_doc("Supplier", {"email": user})

        query = """
		  WITH working as(
       select
              supplier,
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Working'
       group by
              item_group,
               equipment_status
),
ideal as(
       select
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Ideal'
       group by
              item_group
),
breakdown as(
       select
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Breakdown'
       group by
              item_group
),
occupied as(
       select
              item_group,
         equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Occupied With Migoo'
       group by
              item_group
),
free as(
       select
              item_group,
              equipment_status
       from
              `tabItem`
       where
              equipment_status = 'Free'
       group by
              item_group
)
           select
       ig.item_group_name,
       count(i.item_group) as 'Total',
       count(working.equipment_status) as 'Working',
       count(ideal.equipment_status) as 'Ideal',
       count(breakdown.equipment_status) as 'BreakDown',
       count(free.equipment_status) as 'Free',
        i.supplier as 'S:Link/Supplier:-10'
from
       `tabItem Group` ig
       left outer JOIN `tabItem` i ON i.item_group = ig.item_group_name
       left outer JOIN working on ig.item_group_name = working.item_group
       and working.equipment_status = i.equipment_status
       left outer JOIN ideal on ig.item_group_name = ideal.item_group
       and ideal.equipment_status = i.equipment_status
       left outer JOIN breakdown on ig.item_group_name = breakdown.item_group
       and breakdown.equipment_status = i.equipment_status

       left outer JOIN free on ig.item_group_name = free.item_group
       and free.equipment_status = i.equipment_status
where
       ig.parent_item_group = 'All Equipment Groups' 
       AND i.supplier_email = %(supplier_email)s	


group by
       ig.item_group_name
        """

        query_params = {
            "supplier_email": supplier.email,
        }
        print(query_params)

        data = frappe.db.sql(query, query_params, as_dict=True)

    return columns, data
