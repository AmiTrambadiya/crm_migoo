# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import frappe
from frappe import _
import frappe.defaults

@frappe.whitelist()
def status_change(name,status,price,equipment_current_reading,test,img1):
    c = int(status)
    test1=test.split(",")
    if c==0:
        # frappe.msgprint(b)
        frappe.db.set_value("Web item",name,"item_status","Unpublish")
    if c==1:
        # frappe.msgprint(b)
        frappe.db.set_value("Web item",name,"item_status","Publish")
        
    # # record =  frappe.get_list('web Item Slide Show',filters={'parent':a},ignore_permissions=True)
    frappe.db.delete('web Item Slide Show',filters={'parent':name})
    doc = frappe.get_doc('Web item', name)
    for i in test1:
        if i!="":
            doc.append('web_item_slide_show', {
            'image': i,
           #  'request_type':request
            })
            doc.save()
            frappe.db.commit()

    frappe.db.set_value("Web item",name,"price",price)
    frappe.db.set_value("Web item",name,"website_image",img1)
    frappe.db.set_value("Web item",name,"equipment_current_reading",equipment_current_reading)
    