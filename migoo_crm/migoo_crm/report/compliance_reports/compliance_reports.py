import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("Equipment"),
            "fieldname": "name",
            "fieldtype": "link",
            "options": "Item",
            "width": 150,
        },
        {
            "label": _("RTO Registeration No"),
            "fieldname": "register_no",
            "fieldtype": "Data",
            "width": 150,
        },

        {
            "label": _("Model"),
            "fieldname": "Model",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Insurance Last Date"),
            "fieldname": "insurance_date",
            "fieldtype": "Date",
            "width": 150,
        },

        {
            "label": _("Fitness Last Date"),
            "fieldname": "fitness_dt",
            "fieldtype": "Date",
            "width": 150,
        },

        {
            "label": _("PUC Last Date"),
            "fieldname": "pollution",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": _("Completion Date"),
            "fieldname": "Completion Date",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _(""),
            "fieldname": "aaa",
            "fieldtype": "Data",

        },
    ]

    return columns


def get_data(filters):
    return frappe.db.sql(
        """
        with a as(
        select
            name as 'nm',
            insurance_date as 'id',
            TIMESTAMPDIFF(DAY, now(), insurance_date) as 'insurance'
        from
            `tabItem`
        order by
            creation desc
        ),
        aa as(
            select
                nm,
                id,
                concat(
                    'Insurance',
                    ' - ',
                    `insurance`,
                    ' ',
                    'Days to go'
                ) as 'InsuranceCompleteDaysAfter'
        from
            a
        where
            id >= now() - interval 1 day
            and id <= now() + interval 30 day
        ),
        b as(
            select
                name as 'nm1',
                fitness_dt as 'ft',
                TIMESTAMPDIFF(DAY, now(), fitness_dt) as 'fitness'
            from
                `tabItem`
        ),
        bb as(
            select
                nm1,
                ft,
                concat('Fitness', ' - ', `fitness`, ' ', 'Days to go') as 'FitnessCompleteDaysAfter'
            from
            b
        where
            ft >= now() - interval 1 day
            and ft <= now() + interval 30 day
        ),  
        c as(
            select
                name as 'nm2',
                pollution as 'pl',
                TIMESTAMPDIFF(DAY, now(), pollution) as 'pollution'
            from
                `tabItem`
        ),
        cc as(
            select
                nm2,
                pl,
                concat('PUC', ' - ', `pollution`, ' ', 'Days to go') as 'PUCCompleteDaysAfter'
            from
                c
            where
                pl >= now() - interval 1 day
                and pl <= now() + interval 30 day
        )
        select
            `tabItem`.name,
            `tabItem`.register_no,
            `tabItem`.model as 'Model',
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.register_no,
            `tabItem`.model,
            InsuranceCompleteDaysAfter as 'Completion Date',
            concat(
                '<button class="btn btn-primary pt-0 pb-0 compliance-custom-event" data-name="',
                `tabItem`.name,
                '">Update</button>'
            ) as 'aaa'
        from
            `tabItem`
            left join aa on `tabItem`.name = nm
            left join bb on `tabItem`.name = nm1
            left join cc on `tabItem`.name = nm2
        where
            `tabItem`.rto_register = 'Registered'
            and (
                DATE(insurance_date) between %(from_date) s
                and %(to_date) s
            )
        union
        select
            `tabItem`.name,
            `tabItem`.register_no,
            `tabItem`.model as 'Model',
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.register_no,
            `tabItem`.model,
            FitnessCompleteDaysAfter as 'Completion Date',
            concat(
                '<button class="btn btn-primary pt-0 pb-0 compliance-custom-event" data-name="',
                `tabItem`.name,
                '">Update</button>'
            ) as 'aaa'
        from
            `tabItem`
            left join aa on `tabItem`.name = nm
            left join bb on `tabItem`.name = nm1
            left join cc on `tabItem`.name = nm2
        where
            `tabItem`.rto_register = 'Registered'
            and (
                DATE(insurance_date) between %(from_date) s
        and %(to_date) s
        )
        union
        select
            `tabItem`.name,
            `tabItem`.register_no,
            `tabItem`.model as 'Model',
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.register_no,
            `tabItem`.model,
            PUCCompleteDaysAfter as 'Completion Date',
            concat(
                '<button class="btn btn-primary pt-0 pb-0 compliance-custom-event" data-name="',
                `tabItem`.name,
                '">Update</button>'
            ) as 'aaa'
        from
            `tabItem`
            left join aa on `tabItem`.name = nm
            left join bb on `tabItem`.name = nm1
            left join cc on `tabItem`.name = nm2
        where
            `tabItem`.rto_register = 'Registered'
            and (
                DATE(insurance_date) between %(from_date) s
                and %(to_date) s
            )
        union
        select
            `tabItem`.name,
            `tabItem`.register_no,
            `tabItem`.equipment_model_no as 'Model',
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.register_no,
            `tabItem`.model,
            InsuranceCompleteDaysAfter as 'Completion Date',
            concat(
                '<button class="btn btn-primary pt-0 pb-0 compliance-custom-event" data-name="',
                `tabItem`.name,
                '">Update</button>'
            ) as 'aaa'
        from
            `tabItem`
            left join aa on `tabItem`.name = nm
            left join bb on `tabItem`.name = nm1
            left join cc on `tabItem`.name = nm2
        where
            `tabItem`.rto_register = 'Not Registered'
            and (
                DATE(insurance_date) between %(from_date) s
                and %(to_date) s
            )
        		{conditions}
        """
        .format(conditions=get_conditions(filters)
                ),
        filters,
        as_dict=1,
    )


def get_conditions(filters):
    conditions = []

    if filters.get("territory"):
        conditions.append(" and `tabLead`.territory=%(territory)s")

    if filters.get("status"):
        conditions.append(" and `tabLead`.status=%(status)s")

    return " ".join(conditions) if conditions else ""
