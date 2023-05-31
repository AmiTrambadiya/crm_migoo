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
                SUM(CASE WHEN equipment_status = 'Free' THEN 1 ELSE 0 END) AS 'Free',
                SUM(CASE WHEN equipment_status = 'Working' THEN 1 ELSE 0 END) AS 'Working',
                SUM(CASE WHEN equipment_status = 'Ideal' THEN 1 ELSE 0 END) AS 'Ideal',
                SUM(CASE WHEN equipment_status = 'Breakdown' THEN 1 ELSE 0 END) AS 'Breakdown',
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
        current_user = frappe.session.user
        user_doc = frappe.get_doc("User", current_user)
        mobile_number = user_doc.mobile_no
        query = frappe.db.sql("""
            SELECT 
                `tabItem`.item_group AS 'Category',
                `tabItem Group`.item_group_name AS 'subCategory',
                SUM(CASE WHEN equipment_status = 'Free' THEN 1 ELSE 0 END) AS 'Free',
                SUM(CASE WHEN equipment_status = 'Working' THEN 1 ELSE 0 END) AS 'Working',
                SUM(CASE WHEN equipment_status = 'Ideal' THEN 1 ELSE 0 END) AS 'Ideal',
                SUM(CASE WHEN equipment_status = 'Breakdown' THEN 1 ELSE 0 END) AS 'Breakdown',
                COALESCE(COUNT(`tabItem`.equipment_main_category), 0) AS 'Totalss' 
            FROM 
                `tabItem Group`
            LEFT JOIN `tabItem` 
                ON `tabItem Group`.item_group_name = `tabItem`.equipment_main_category
            AND (`tabItem`.supplier_email = %s or `tabItem`.supplier_number=%s)
            WHERE 
                `tabItem Group`.parent_item_group != 'All Equipment Groups'
            AND `tabItem Group`.parent_item_group = %s
            GROUP BY 
                `tabItem Group`.item_group_name

    """, (current_user, mobile_number, main_category),  as_dict=True)

    return query, main_category
