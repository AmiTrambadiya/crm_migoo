import frappe
import datetime
from frappe.utils import now, getdate


@frappe.whitelist()
def send_daily_mail_report():
    new_supplier = frappe.db.sql(
        "select count(name)as Supplier from `tabSupplier` where creation >= now() - INTERVAL 9 hour and HOUR(creation) in (10,11,12,13,14,15,16,17,18,19)", as_list=True)
    new_equipment = frappe.db.sql("select count(name)as Equipment from `tabItem` where creation >= now() - INTERVAL 9 hour and HOUR(creation) in (10,11,12,13,14,15,16,17,18,19)", as_list=True)
    total_supplier = frappe.db.get_list("Supplier")
    total_equipment = frappe.db.get_list("Item")
    today = frappe.utils.get_datetime(getdate()).strftime("%d-%b-%Y")

    recipients = [
        'arjun.pachani@gmail.com',
        'kamal@sanskartechnolab.com'
    ]

    message = f'''
        <p>Respected Management,</p>
        <p>The updates as of {today} are</p>
        <p>New Supplier Added: {new_supplier[0][0]}</p>
        <p>New Equipment Added: {new_equipment[0][0]}</p>
        <p>Total Supplier: {len(total_supplier)}</p>
        <p>Total Equipment: {len(total_equipment)}</p>
    '''

    frappe.sendmail(
        recipients=recipients,
        subject='Daily Report',
        message=message
    )