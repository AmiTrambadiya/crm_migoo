import frappe
from datetime import datetime, timedelta

@frappe.whitelist(allow_guest=1)
def execute(filters=None):
    columns = [
        {
            "label": "Period",
            "fieldname": "period",
            "fieldtype": "Data",
            "width": 160
        },
        {
            "label": "Item",
            "fieldname": "item",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Supplier",
            "fieldname": "supplier",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Lead",
            "fieldname": "lead",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Opportunity",
            "fieldname": "opportunity",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Quotation",
            "fieldname": "quotation",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Call logs",
            "fieldname": "call_logs_created",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Customer",
            "fieldname": "customer",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "User",
            "fieldname": "user",
            "fieldtype": "Int",
            "width": 120
        }
    ]

    data = []
    start_date = datetime.strptime(filters.get('start_date'), '%d-%m-%Y').date() if filters.get(
        'start_date') else datetime.now().date().replace(day=1, month=1) - timedelta(days=7)
    end_date = datetime.strptime(filters.get(
        'end_date'), '%d-%m-%Y').date() if filters.get('end_date') else datetime.now().date()
    current_date = datetime.now().date()

    if filters.get('period') == 'Daily':

        if filters.get('from_date'):
            start_date = datetime.strptime(
                filters.get('from_date'), '%Y-%m-%d').date()
        if filters.get('to_date'):
            end_date = datetime.strptime(
                filters.get('to_date'), '%Y-%m-%d').date()

        while start_date <= end_date:
            if start_date <= current_date:

                item = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabItem`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                supplier = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabSupplier`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                lead = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabLead`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                opportunity = frappe.db.sql("""
			    	SELECT COUNT(*) FROM `tabOpportunity`
			    	WHERE DATE(`creation`) = '{0}'
			    """.format(start_date))[0][0] or 0

                quotation = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabQuotation`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                call_logs_created = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabCall Log`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                customer = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabCustomer`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                user = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabUser`
                    WHERE DATE(`creation`) = '{0}'
                """.format(start_date))[0][0] or 0

                data.append({
                    "period": start_date.strftime('%d-%m-%Y'),
                    "supplier": supplier,
                    "lead": lead,
                    "opportunity": opportunity,
                    "quotation": quotation,
                    "call_logs_created": call_logs_created,
                    "customer": customer,
                    "item": item,
                    "user": user
                })
                start_date += timedelta(days=1)

            data.sort(key=lambda x: datetime.strptime(
                x["period"], "%d-%m-%Y"), reverse=True)

    elif filters.get('period') == 'Weekly':
        if filters.get('from_date'):
            start_date = datetime.strptime(
                filters.get('from_date'), '%Y-%m-%d').date()
        if filters.get('to_date'):
            end_date = datetime.strptime(
                filters.get('to_date'), '%Y-%m-%d').date()
        while start_date <= end_date:
            week_start = start_date - timedelta(days=start_date.weekday())
            week_end = week_start + timedelta(days=6)

            if week_start > end_date:
                break

            item = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabItem`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(week_start, week_end))[0][0] or 0

            supplier = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabSupplier`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(week_start, week_end))[0][0] or 0

            lead = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabLead`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(week_start, week_end))[0][0] or 0

            call_logs_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCall Log`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(start_date, week_end))[0][0] or 0

            opportunity = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabOpportunity`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(week_start, week_end))[0][0] or 0

            quotation = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabQuotation`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(week_start, week_end))[0][0] or 0

            customer = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCustomer`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(week_start, week_end))[0][0] or 0

            user = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabUser`
                    WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
                """.format(week_start, week_end))[0][0] or 0

            data.insert(0, {
                "period": "{0} - {1}".format(week_start.strftime('%d-%m-%Y'), week_end.strftime('%d-%m-%Y')),
                "lead": lead,
                "supplier": supplier,
                "call_logs_created": call_logs_created,
                "opportunity": opportunity,
                "quotation": quotation,
                "customer": customer,
                "item": item,
                "user": user
            })
            start_date = week_end + timedelta(days=1)

    elif filters.get('period') == 'Monthly':

        if filters.get('from_date'):
            start_date = datetime.strptime(filters.get(
                'from_date'), '%Y-%m-%d').date().replace(day=1)
        if filters.get('to_date'):
            end_date = datetime.strptime(filters.get(
                'to_date'), '%Y-%m-%d').date().replace(day=1)

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
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(month_start, month_end))[0][0] or 0

            supplier = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabSupplier`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(month_start, month_end))[0][0] or 0

            lead = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabLead`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
            """.format(month_start, month_end))[0][0] or 0

            call_logs_created = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabCall Log`
                WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
                """.format(start_date, month_end))[0][0] or 0

            opportunity = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabOpportunity`
                    WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
                    """.format(month_start, month_end))[0][0] or 0

            quotation = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabQuotation`
                    WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
                    """.format(month_start, month_end))[0][0] or 0

            customer = frappe.db.sql("""
                    SELECT COUNT(*) FROM `tabCustomer`
                    WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
                    """.format(month_start, month_end))[0][0] or 0

            user = frappe.db.sql("""
                        SELECT COUNT(*) FROM `tabUser`
                         WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
                    """.format(month_start, month_end))[0][0] or 0

            data.insert(0, {
                "period": start_date.strftime('%m-%Y'),
                "lead": lead,
                "supplier": supplier,
                "call_logs_created": call_logs_created,
                "opportunity": opportunity,
                "quotation": quotation,
                "customer": customer,
                "item": item,
                "user": user
            })
            start_date = month_end + timedelta(days=1)

    return columns, data


# def get_week_wise_data_with_filter(from_date, to_date):
#     # Get the current week start and end dates.
#     week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - \
#         timedelta(days=week_start.weekday())
#     week_end = week_start + timedelta(days=6)

#     # Use the `frappe.db.sql()` function to query the database for the data between the from date and to date.
#     query = """
#         SELECT COUNT(*) AS total
#         FROM `tabItem`
#         WHERE DATE(`creation`) BETWEEN '{0}' AND '{1}'
#     """.format(week_start, week_end)
#     results = frappe.db.sql(query)

#     # Filter the results by the week start and end dates.
#     filtered_results = []
#     for result in results:
#         if week_start <= result[0] <= week_end:
#             filtered_results.append(result)

#     # Return the filtered results.
#     return filtered_results


# def get_week_wise_data(filters):
#     # Check if the `period` filter is set to `Weekly`.
#     if filters.get('period') == 'Weekly':
#         # Get the from date and to date from the filters.
#         from_date = filters.get('from_date')
#         to_date = filters.get('to_date')

#         # Get the week wise data with filter for from date and to date.
#         data = get_week_wise_data_with_filter(from_date, to_date)

#         # Return the data.
#         return data

#     # If the `period` filter is not set to `Weekly`, return the original data.
#     # return data
