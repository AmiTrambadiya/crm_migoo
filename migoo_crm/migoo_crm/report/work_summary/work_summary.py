# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime
from erpnext.buying.doctype.supplier.supplier import Supplier
from erpnext.telephony.doctype.call_log.call_log import CallLog
from erpnext.crm.doctype.lead.lead import Lead
from erpnext.crm.doctype.opportunity.opportunity import Opportunity
from erpnext.selling.doctype.quotation.quotation import Quotation
from erpnext.selling.doctype.customer.customer import Customer

def execute(filters=None):
    columns = [
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 200
        },
        {
            "label": _("Equipment"),
            "fieldname": "items_created	",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": _("Supplier"),
            "fieldname": "suppliers_created",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": _("Call logs"),
            "fieldname": "call_logs_created",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": _("Lead"),
            "fieldname": "leads_created",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": _("Opportunity"),
            "fieldname": "Opportunity_created",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": _("Quotation"),
            "fieldname": "Quotation_created",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": _("Customer"),
            "fieldname": "Customer_created",
            "fieldtype": "Int",
            "width": 125
        },
    ]

    data = []

    from_date_str = filters.get("from_date")
    to_date_str = filters.get("to_date")

    if from_date_str and to_date_str:
        from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d")
        to_date = datetime.datetime.strptime(to_date_str, "%Y-%m-%d")
        while from_date <= to_date:
            
            items_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabItem`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            suppliers_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabSupplier`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            call_logs_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCall Log`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            leads_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabLead`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            Opportunity_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabOpportunity`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            Quotation_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabQuotation`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            Customer_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCustomer`
                WHERE DATE(`creation`) = %s
            """, (from_date.strftime("%Y-%m-%d"),))[0][0] or 0

            data.append({
                "date":from_date.strftime("%Y-%m-%d"),
                "items_created":items_created,
                "suppliers_created": suppliers_created,
                "call_logs_created": call_logs_created,
                "leads_created": leads_created,
                "Opportunity_created": Opportunity_created,
                "Quotation_created": Quotation_created,
				"Customer_created": Customer_created
            })
            from_date += datetime.timedelta(days=1)

    return columns, data