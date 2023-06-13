# Copyright (c) 2023, Palak Padalia and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SummarySheet(Document):
	pass


@frappe.whitelist()
def get_logsheet_data(name,from_time,to_time,equipment,customer):
	name1= frappe.db.sql("""SELECT name FROM `tabLog Sheet` WHERE  equipment=%s AND customer=%s AND date BETWEEN %s AND %s """,(equipment,customer,from_time,to_time))
	nm=[]
	total_working_time=0.0
	overtime_calculation=0.0
	total_ideal_time=0.0
	total_breckdown_time=0.0
	total_time=0.0
	total_km=0.0
	total_hours=0.0
	total_fuel=0.0
	for i in name1:
		for j in i:
			nm.append(j)
	for i1 in nm:
		log=frappe.get_doc("Log Sheet", i1)

		total_working_time = total_working_time + log.total_working_time
		overtime_calculation = overtime_calculation + log.overtime_calculation
		total_ideal_time = total_ideal_time + log.total_ideal_time
		total_breckdown_time = total_breckdown_time + log.total_breckdown_time
		total_time = total_time + log.total_time
		total_km = total_km + log.total_km
		total_hours = total_hours + log.total_hours
		total_fuel = total_fuel + log.total_fuel


		dict1 = {"total_working_time":total_working_time,"overtime_calculation":overtime_calculation,"total_ideal_time":total_ideal_time,"total_breckdown_time":total_breckdown_time,"total_time":total_time,"total_km":total_km,"total_hours":total_hours,"total_fuel":total_fuel}
	return dict1
			
@frappe.whitelist()
def get_rate(parent,item_code):
	e_rata = frappe.db.sql("select rate from `tabSales Order Item` where parent=%s and item_code=%s",(parent,item_code))
	rate=0
	for i in e_rata:
		for j in i:
			rate=j
	return rate
