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
        frappe.db.set_value("Web item",name,"publish",0)
    if c==1:
        # frappe.msgprint(b)
        frappe.db.set_value("Web item",name,"publish",1)
        
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
    
@frappe.whitelist()
def address_update(name,address_line1,city,state,postal_code):
    titile= name + "-Billing"
    frappe.msgprint(state)
    frappe.db.set_value("Address",titile,"address_line1",address_line1)
    # frappe.db.set_value("Address",titile,"address_line2",address_line2)
    frappe.db.set_value("Address",titile,"city",city)
    frappe.db.set_value("Address",titile,"state",state)
    # frappe.db.set_value("Address",titile,"area",area)
    frappe.db.set_value("Address",titile,"pincode",postal_code)
    frappe.response["msg"]="Address Updated"