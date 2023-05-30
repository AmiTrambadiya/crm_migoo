import frappe
from frappe import _


@frappe.whitelist(allow_guest=1)
def ChildCategories():
    user = frappe.session.user

    if 'System Manager' in frappe.get_roles(user):

        query = frappe.db.sql("""
        select 
            parent_item_group,
            item_group_name,
            count(equipment_category)

        from `tabItem`

        right join `tabItem Group` on 
                `tabItem Group`.item_group_name =  `tabItem`.equipment_category

        where 
            parent_item_group 
            not in(
                'All Equipment Groups',
                'Aerial Work Platform',
                'Concrete Machinery',
                'Cranes',
                'Earth Moving Machinery',
                'Truck / Tanker / Trailor',
                'Road Machinery',
                'Lifting and Handling Machinery',
                'Miscellaneous',
                'Plant Crushing and Screening')

            and item_group_name!='All Equipment Groups'

        group by item_group_name
        
    """, (),  as_dict=True)

    return query
