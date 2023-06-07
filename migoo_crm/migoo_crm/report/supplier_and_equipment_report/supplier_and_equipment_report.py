# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def execute(filters=None):
    columns = [
        {
            "label": _("Supplier"),
            "fieldname": "Supplier",
            "width": 200,
            "fieldtype": "Link",
            "options": "Supplier",
        },
        {
            "label": _("Supplier Company"),
            "fieldname": "SupplierCompany",
            "width": 220,
        },
        {
            "label": _("Supplier Creation Date"),
            "fieldname": "SupplierCreationDate",
            "width": 160,
        },
        {
            "label": _("1st Equipment of Supplier"),
            "fieldname": "1stEquipmentofSupplier",
            "width": 160,
        },
        {
            "label": _("1st Equipment Created By Supplier"),
            "fieldname": "1stEquipmentCreatedBySupplier",
            "width": 180,
        },
        {
            "label": _("Creation Difference of Supplier and 1st Equipment"),
            "fieldname": "CreationDifferenceofSupplierand1stEquipment",
            "width": 200,
        },

    ]

    data = []
    query = """
        WITH 
        difference_in_seconds AS (
    	select
			s.name as 'suppliername',
        	date(s.creation) as 'SupplierCreatedDate',
        	s.supplier_name as 'Supplier',
            s.company_name as 'SupplierCompany',
        	i.name as '1stEquipment',
        	date(i.creation) as 'EquipmentCreatedDate',
        	TIMESTAMPDIFF(SECOND, s.creation, i.creation) AS seconds
    	from
        	`tabSupplier` s
        inner join `tabItem` i on s.name = i.supplier
        
        where s.verify='Verify'
		),
		differences AS (
    	SELECT
			suppliername as 'suppliernames',
        	Supplier as 's',
            SupplierCompany as 'sc',
        	SupplierCreatedDate as 'a',
        	1stEquipment as 'b',
        	EquipmentCreatedDate as 'c',
        	seconds,
        	MOD(seconds, 60) AS seconds_part,
        	MOD(seconds, 3600) AS minutes_part,
        	MOD(seconds, 3600 * 24) AS hours_part
    	FROM
        	difference_in_seconds
		)
		select
    		s as 'Supplier',
            sc as 'SupplierCompany',
    		a as 'SupplierCreationDate',
    		b as '1stEquipmentofSupplier',
            suppliernames as 'SN',
    		c as '1stEquipmentCreatedBySupplier',
    		CONCAT(
    		    FLOOR(seconds / 3600 / 24),
    		    ' days ',
    		    FLOOR(hours_part / 3600),
    		    ' hours ',
    		    FLOOR(minutes_part / 60),
    		    ' minutes ',
    		    seconds_part,
    		    ' seconds'
    		) AS 'CreationDifferenceofSupplierand1stEquipment'
		FROM
    		differences
    """

    

    if filters and filters.get("suppliernames"):
        query += " WHERE suppliernames = %(suppliernames)s"

    query += """
        GROUP BY
            s
        ORDER BY
            c DESC
    """

    data = frappe.db.sql(query, filters, as_dict=1)

    return columns, data
