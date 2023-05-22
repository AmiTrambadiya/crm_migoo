# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {
            "label": _("Equipment Name"),
            "fieldname": "EquipmentName",
            "width": 140,
        },
        {
            "label": _("Equipment Sub Category"),
            "fieldname": "EquipmentSubCategory",
            "width": 140,
        },
        {
            "label": _("Email Send Date"),
            "fieldname": "EmailSendDate",
            "width": 140,
        },
        {
            "label": _("Insurance Date"),
            "fieldname": "InsuranceDate",
            "width": 140,
        },
        {
            "label": _("Supplier Name"),
            "fieldname": "SupplierName",
            "width": 140,
        },
        {
            "label": _("Supplier Whatsapp No"),
            "fieldname": "SupplierWhatsappNo",
            "width": 140,
        },
        {
            "label": _("Supplier Email"),
            "fieldname": "SupplierEmail",
            "width": 140,
        },
        {
            "label": _("Email Status"),
            "fieldname": "EmailStatus",
            "width": 140,
        },
    ]

    data = []
    query = """
			select
			    eq.reference_name as 'EquipmentName',
			    i.equipment_main_category as 'EquipmentSubCategory',
			    date(eq.creation) as 'EmailSendDate',
			    i.insurance_date as 'InsuranceDate',
			    i.supplier_name as 'SupplierName',
			    i.whatsapp_no as 'SupplierWhatsappNo',
			    i.supplier_email as 'SupplierEmail',
			    eq.status as 'EmailStatus'
			from
			    `tabEmail Queue` eq
            inner join `tabItem` i 
			on eq.reference_name=i.name
			where 
            	eq.reference_doctype='Item' 
    """

    if filters and filters.get("from_date") and filters.get("to_date"):
        query += " and DATE(eq.creation) BETWEEN %(from_date)s AND %(to_date)s"

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
