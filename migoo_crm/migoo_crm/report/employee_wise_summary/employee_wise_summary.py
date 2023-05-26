# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@frappe.whitelist(allow_guest=1)
def execute(filters=None):
    columns = [
        {
            "label": "Period",
            "fieldname": "period",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Item",
            "fieldname": "item",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": "Supplier",
            "fieldname": "supplier",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": "Lead",
            "fieldname": "lead",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": "Opportunity",
            "fieldname": "opportunity",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": "Quotation",
            "fieldname": "quotation",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": "Call logs",
            "fieldname": "call_logs_created",
            "fieldtype": "Int",
            "width": 125
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Int",
            "width": 125
        }
    ]

    data = []
    start_date = datetime.strptime(filters.get('start_date'), '%d-%m-%Y').date() if filters.get(
        'start_date') else datetime.now().date().replace(day=1, month=1) - timedelta(days=7)
    end_date = datetime.strptime(filters.get(
        'end_date'), '%d-%m-%Y').date() if filters.get('end_date') else datetime.now().date()
    user = filters.get('user') if filters and 'user' in filters else None
    if filters.get('period') == 'Daily':
        while start_date <= end_date:
            item = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabItem`
                WHERE DATE(`creation`) = '{0}' {1}
            """.format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            supplier = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabSupplier`
                WHERE DATE(`creation`) = '{0}' {1}
            """.format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            lead = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabLead`
                WHERE DATE(`creation`) = '{0}' {1}
            """.format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            opportunity = frappe.db.sql("""
				SELECT COUNT(*) FROM `tabOpportunity`
				WHERE DATE(`creation`) = '{0}' {1}
			""".format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            quotation = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabQuotation`
                WHERE DATE(`creation`) = '{0}' {1}
            """.format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            call_logs_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCall Log`
                WHERE DATE(`creation`) = '{0}' {1}
            """.format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            customer = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCustomer`
                WHERE DATE(`creation`) = '{0}' {1}
            """.format(start_date, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            data.append({
                "period": start_date.strftime('%d-%m-%Y'),
                "supplier": supplier,
                "lead": lead,
                "opportunity": opportunity,
                "quotation": quotation,
                "call_logs_created": call_logs_created,
                "customer": customer,
                "item": item
            })
            start_date += timedelta(days=1)
            data = sorted(data, key=lambda x: datetime.strptime(
                x['period'], '%d-%m-%Y'), reverse=True)

    elif filters.get('period') == 'Weekly':
        while start_date <= end_date:
            week_start = start_date - timedelta(days=start_date.weekday())
            week_end = week_start + timedelta(days=6)
            item = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabItem`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(week_start, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            supplier = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabSupplier`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(week_start, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            lead = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabLead`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(week_start, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            call_logs_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCall Log`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(start_date, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            opportunity = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabOpportunity`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(week_start, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            quotation = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabQuotation`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(week_start, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            customer = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCustomer`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(week_start, week_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            data.append({
                "period": "{0} - {1}".format(week_start.strftime('%d-%m-%Y'), week_end.strftime('%d-%m-%Y')),
                "lead": lead,
                "supplier": supplier,
                "call_logs_created": call_logs_created,
                "opportunity": opportunity,
                "quotation": quotation,
                "customer": customer,
                "item": item
            })
            start_date = week_end + timedelta(days=1)

            data.sort(key=lambda x: datetime.strptime(
                x["period"].split(" - ")[0], "%d-%m-%Y"), reverse=True)

    elif filters.get('period') == 'Monthly':
        current_date = datetime.now().date()
    #    start_date = datetime(current_date.year - 1, 1, 1).date()
        start_date = datetime(2022, 12, 1).date()
        end_date = (current_date + relativedelta(months=1)
                    ).replace(day=1) - timedelta(days=1)
        while start_date <= end_date:
            year_month = start_date.strftime('%m-%Y')
            month_start = datetime.strptime(
                year_month + '-01', '%m-%Y-%d').date()
            month_end = month_start.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)
            if month_end < month_start:
                month_end = month_end + timedelta(days=month_end.day)
                month_end = min(month_end, end_date)

            item = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabItem`
            WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
        """.format(month_start, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            supplier = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabSupplier`
            WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
        """.format(month_start, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            lead = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabLead`
            WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
        """.format(month_start, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            call_logs_created = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabCall Log`
            WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
            """.format(start_date, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            opportunity = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabOpportunity`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
                """.format(month_start, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            quotation = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabQuotation`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
                """.format(month_start, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            customer = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCustomer`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}' {2}
                """.format(month_start, month_end, f"AND owner = '{user}'" if user else ""))[0][0] or 0

            data.append({
                "period": start_date.strftime('%m-%Y'),
                "lead": lead,
                "supplier": supplier,
                "call_logs_created": call_logs_created,
                "opportunity": opportunity,
                "quotation": quotation,
                "customer": customer,
                "item": item
            })
            start_date = month_end + timedelta(days=1)
            data = sorted(data, key=lambda x: datetime.strptime(
                x['period'], '%m-%Y'), reverse=True)

    return columns, data
