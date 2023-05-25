import frappe
from frappe import _


def execute(filters=None):
    columns = [
        _("Name") + ":Data:170",
        _("Phone No") + ":Data:170",
        _("User") + ":Int:120",
        _("Equipment") + ":Int:120",
        _("Supplier") + ":Int:120",
        _("Call Logs") + ":Int:120",
        _("Lead") + ":Int:120",
        _("Opportunity") + ":Int:120",
        _("Quotation") + ":Int:120",
    ]

    data = []
    sales_team_users = frappe.db.sql(
        """select name,phone from `tabUser` where module_profile='Sales Team' and enabled=1""",  as_dict=1,
    )

    for user in sales_team_users:
        name = user.name
        phone = user.phone

        user_count = frappe.db.count("User", {"owner": name, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        equipment_count = frappe.db.count("Item", {"owner": name, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        supplier_count = frappe.db.count("Supplier", {"owner_name": name, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        call_logs_count = frappe.db.count("Call Logs", {"agent_number": phone, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        lead_count = frappe.db.count("Lead", {"lead_owner": name, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        opportunity_count = frappe.db.count("Opportunity", {"opportunity_owner": name, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        quotation_count = frappe.db.count("Quotation", {"owner": name, "creation": (
            "between", [filters.get("from_date"), filters.get("to_date")])})

        row = [name, phone, user_count, equipment_count, supplier_count,
               call_logs_count, lead_count, opportunity_count, quotation_count]
        data.append(row)

    return columns, data
