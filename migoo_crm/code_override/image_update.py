# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import frappe
from frappe import _
import frappe.defaults

@frappe.whitelist()
def status_change(name,sub,test,img1,img2,img3,img4,img5,img6,insurance_date):
    
    test1=test.split(",")
    list1=[img1,img2,img3,img4,img5,img6]
    # # record =  frappe.get_list('web Item Slide Show',filters={'parent':a},ignore_permissions=True)
    frappe.db.delete('web Item Slide Show',filters={'parent':name})
    doc = frappe.get_doc('Web item', name)
    for j in list1:
        if j!="":
            doc.append('web_item_slide_show', {
            'image': j,
           #  'request_type':request
            })
            doc.save()
            frappe.db.commit()
    for i in test1:
        if i!="":
            doc.append('web_item_slide_show', {
            'image': i,
           #  'request_type':request
            })
            doc.save()
            frappe.db.commit()

    frappe.db.set_value("Web item",name,"web_item_name",sub)
    # frappe.db.set_value("Web item",name,"model",model)
    frappe.db.set_value("Web item",name,"website_image",img1)
    frappe.db.set_value("Web item",name,"insurance_date",insurance_date)
    # frappe.db.set_value("Web item",name,"sold_out",sold_out)
    # frappe.db.set_value("Web item",name,"equipment_current_reading",equipment_current_reading)
    
@frappe.whitelist()
def address_update(name,address_line1,city,state,postal_code):
    titile= name + "-Billing"
    frappe.db.set_value("Address",titile,"address_line1",address_line1)
    # frappe.db.set_value("Address",titile,"address_line2",address_line2)
    frappe.db.set_value("Address",titile,"city",city)
    frappe.db.set_value("Address",titile,"state",state)
    # frappe.db.set_value("Address",titile,"area",area)
    frappe.db.set_value("Address",titile,"pincode",postal_code)
    frappe.response["msg"]="Address Updated"
