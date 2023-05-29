import frappe


@frappe.whitelist(allow_guest=True)
def role_check(user):
    d = frappe.db.get_value('User', user, 'role_profile_name')
    # d1=frappe.db.get_value('Supplier', filters={"email":user})
    frappe.response["role"] = d
    # frappe.msgprint(d)
    frappe.response["supplier"] = d
