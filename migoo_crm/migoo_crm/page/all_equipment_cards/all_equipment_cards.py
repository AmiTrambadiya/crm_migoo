import frappe
from frappe import _


@frappe.whitelist(allow_guest=1)
def AllEquipments(main_category):

    user = frappe.session.user

    if 'System Manager' in frappe.get_roles(user):

        query = frappe.db.sql("""
            select 
                item_group,
                item_group_name as 'subCategory',
                count(equipment_main_category) as 'Totalss' 

            from `tabItem`

            right join `tabItem Group` on 
                `tabItem Group`.item_group_name =  `tabItem`.equipment_main_category

            where parent_item_group !='All Equipment Groups'
                and parent_item_group=%s

            group by 
                item_group_name
        
    """, (main_category),  as_dict=True)

    else:
        query = frappe.db.sql("""
            select 
                item_group,
                item_group_name as 'subCategory',
                count(equipment_main_category) as 'Totalss' 

            from `tabItem`

            right join `tabItem Group` on 
                `tabItem Group`.item_group_name =  `tabItem`.equipment_main_category

            where parent_item_group !='All Equipment Groups'
                and parent_item_group = %s
                and supplier_email = %s

            group by 
                item_group_name
        
    """, (main_category, user),  as_dict=True)

    return query, main_category