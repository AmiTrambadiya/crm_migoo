import frappe
from frappe import _

# Number Cards
@frappe.whitelist()
def equipment():

    user = frappe.session.user

    if 'System Manager' in frappe.get_roles(user):

        query = frappe.db.sql("""
        select

        `tabItem`.name,
            item_group_name as 'ItemGroup', 
            count(item_group) as 'TotalEquipment',
            supplier_email ,
            `tabItem Group`.add_image as 'Image'

        from
            `tabItem`

        right join `tabItem Group` on 
        `tabItem Group`.item_group_name = `tabItem`.item_group

        where parent_item_group='All Equipment Groups'

        group by
            item_group_name

    """,  as_dict=True)

    else:
        query = frappe.db.sql("""
        select

        `tabItem`.name,
            item_group_name as 'ItemGroup', 
            count(item_group) as 'TotalEquipment',
            supplier_email ,
            `tabItem Group`.add_image as 'Image'

        from
            `tabItem`

        right join `tabItem Group` on 
        `tabItem Group`.item_group_name = `tabItem`.item_group

        where parent_item_group='All Equipment Groups'
        and
        supplier_email = %s

        group by    
            item_group_name

    """, (user,), as_dict=True)

    return query

#Dashboard Chart
@frappe.whitelist()
def get_equipment_by_category():

    user = frappe.session.user

    if 'System Manager' in frappe.get_roles(user):

        data = frappe.db.sql("""
            SELECT equipment_status as label, count(*) as value
            FROM `tabItem`
            GROUP BY equipment_status
        """, as_dict=True)

    else:
        data = frappe.db.sql("""
            SELECT equipment_status as label, count(*) as value
            FROM `tabItem`

            where
            supplier_email = %s
            
            GROUP BY equipment_status
        """, (user,), as_dict=True)

    return data

#Grid Report
@frappe.whitelist()
def get_compliance_report():

    user = frappe.session.user

    if 'System Manager' in frappe.get_roles(user):

        query = frappe.db.sql(
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
                name,
                register_no,
                model as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
                InsuranceCompleteDaysAfter as 'CompletionDate',
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

            union

            select
                name,
                register_no,
                model as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
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

            union

            select
                name,
                register_no,
                model as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
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

            union

            select 
                name,
                register_no,
                equipment_model_no as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
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

            """

        )

        return query

    else:
        query = frappe.db.sql(
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
                name,
                register_no,
                model as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
                InsuranceCompleteDaysAfter as 'CompletionDate',
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
                and supplier_email = %s

            union

            select
                name,
                register_no,
                model as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
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
                 and supplier_email = %s

            union

            select
                name,
                register_no,
                model as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
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
                 and supplier_email = %s

            union

            select 
                name,
                register_no,
                equipment_model_no as 'Model',
                insurance_date,
                fitness_dt,
                pollution,
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
                 and supplier_email = %s

            """, (user, user, user, user)
        )

        return query
