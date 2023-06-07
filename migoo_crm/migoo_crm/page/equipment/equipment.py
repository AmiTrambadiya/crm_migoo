import frappe
from frappe import _

# Number Cards


@frappe.whitelist()
def equipment():

    current_user = frappe.session.user

    if 'System Manager' in frappe.get_roles(current_user):

        query = frappe.db.sql("""
        select

        `tabItem`.name,
            item_group_name as 'ItemGroup',
            count(item_group) as 'TotalEquipment',
            supplier_email ,
            SUM(CASE WHEN equipment_status = 'Free' THEN 1 ELSE 0 END) AS 'Free',
            SUM(CASE WHEN equipment_status = 'Working' THEN 1 ELSE 0 END) AS 'Working',
            SUM(CASE WHEN equipment_status = 'Ideal' THEN 1 ELSE 0 END) AS 'Ideal',
            SUM(CASE WHEN equipment_status = 'Breakdown' THEN 1 ELSE 0 END) AS 'Breakdown',
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
        current_user = frappe.session.user
        user_doc = frappe.get_doc("User", current_user)
        mobile_number = user_doc.mobile_no
        # print(mobile_number)
        query = frappe.db.sql("""
        SELECT
            `tabItem`.name,
            `tabItem Group`.item_group_name AS 'ItemGroup',
            COUNT(`tabItem`.item_group) AS 'TotalEquipment',
            supplier_email,
            SUM(CASE WHEN equipment_status = 'Free' THEN 1 ELSE 0 END) AS 'Free',
            SUM(CASE WHEN equipment_status = 'Working' THEN 1 ELSE 0 END) AS 'Working',
            SUM(CASE WHEN equipment_status = 'Ideal' THEN 1 ELSE 0 END) AS 'Ideal',
            SUM(CASE WHEN equipment_status = 'Breakdown' THEN 1 ELSE 0 END) AS 'Breakdown',
            `tabItem Group`.add_image AS 'Image'
        FROM
            `tabItem Group`
        LEFT JOIN `tabItem` ON
            `tabItem Group`.item_group_name = `tabItem`.item_group
            AND (`tabItem`.supplier_email = %s or `tabItem`.supplier_number=%s)
        WHERE
            `tabItem Group`.parent_item_group = 'All Equipment Groups'
        GROUP BY
            `tabItem Group`.item_group_name, `tabItem`.supplier_email
    """, (current_user,mobile_number), as_dict=True)

    return query

# Dashboard Chart


@frappe.whitelist()
def get_equipment_by_category():

    user = frappe.session.user

    if 'System Manager' in frappe.get_roles(user):

        data = frappe.db.sql("""
            SELECT equipment_status as label, count(*) as value
            FROM `tabItem`
              where
            equipment_status!=''
            GROUP BY equipment_status
          
        """, as_dict=True)

    else:
        user_doc = frappe.get_doc("User", user)
        mobile_number = user_doc.mobile_no

        data = frappe.db.sql("""
            SELECT equipment_status as label, count(*) as value
            FROM `tabItem`

            where
            equipment_status!=''
            and
            (supplier_email = %s or supplier_number=%s)
            

            GROUP BY equipment_status
        """, (user, mobile_number), as_dict=True)

    return data

# Grid Report


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
        ),

        d as(
            select
                name as 'nm3',
                mv_tax_upto as 'mvt',
                TIMESTAMPDIFF(DAY, now(), mv_tax_upto) as 'mvtax'
            from
                `tabItem`
        ),
        dd as(
            select
                nm3,
                mvtax,
                concat('MV Tax', ' - ', `mvtax`, ' ', 'Days to go') as 'MVTaxCompleteDaysAfter'
            from
                d
            where
                mvt >= now() - interval 1 day
                and mvt <= now() + interval 30 day
        ),

        e as(
            select
                name as 'nm4',
                permit_validity_upto as 'spt',
                TIMESTAMPDIFF(DAY, now(), permit_validity_upto) as 'statepermit'
            from
                `tabItem`
        ),
        ee as(
            select
                nm4,
                statepermit,
                concat('State Permit', ' - ', `statepermit`, ' ', 'Days to go') as 'StatePermitCompleteDaysAfter'
            from
                e
            where
                spt >= now() - interval 1 day
                and spt <= now() + interval 30 day
        ),

        f as(
            select
                name as 'nm5',
                npermit_upto as 'npt',
                TIMESTAMPDIFF(DAY, now(), npermit_upto) as 'nationalpermit'
            from
                `tabItem`
        ),
        ff as(
            select
                nm5,
                nationalpermit,
                concat('National Permit', ' - ', `nationalpermit`, ' ', 'Days to go') as 'NationalPermitCompleteDaysAfter'
            from
                f
            where
                npt >= now() - interval 1 day
                and npt <= now() + interval 30 day
        )

        select
            `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
            InsuranceCompleteDaysAfter!=''

        union
        select
            `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           FitnessCompleteDaysAfter!=''

        union
        select
             `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
            PUCCompleteDaysAfter!=''

        union
        select
             `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
            MVTaxCompleteDaysAfter as 'Completion Date',
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           MVTaxCompleteDaysAfter!=''

        union
        select
            `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
            ee.StatePermitCompleteDaysAfter as 'Completion Date',
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           StatePermitCompleteDaysAfter!=''

        union
        select
             `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
            NationalPermitCompleteDaysAfter as 'Completion Date',
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           NationalPermitCompleteDaysAfter!=''

            """

        )
        # print(query)

        return query

    else:

        user_doc = frappe.get_doc("User", user)
        mobile_number = user_doc.mobile_no

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
        ),

        d as(
            select
                name as 'nm3',
                mv_tax_upto as 'mvt',
                TIMESTAMPDIFF(DAY, now(), mv_tax_upto) as 'mvtax'
            from
                `tabItem`
        ),
        dd as(
            select
                nm3,
                mvtax,
                concat('MV Tax', ' - ', `mvtax`, ' ', 'Days to go') as 'MVTaxCompleteDaysAfter'
            from
                d
            where
                mvt >= now() - interval 1 day
                and mvt <= now() + interval 30 day
        ),

        e as(
            select
                name as 'nm4',
                permit_validity_upto as 'spt',
                TIMESTAMPDIFF(DAY, now(), permit_validity_upto) as 'statepermit'
            from
                `tabItem`
        ),
        ee as(
            select
                nm4,
                statepermit,
                concat('State Permit', ' - ', `statepermit`, ' ', 'Days to go') as 'StatePermitCompleteDaysAfter'
            from
                e
            where
                spt >= now() - interval 1 day
                and spt <= now() + interval 30 day
        ),

        f as(
            select
                name as 'nm5',
                npermit_upto as 'npt',
                TIMESTAMPDIFF(DAY, now(), npermit_upto) as 'nationalpermit'
            from
                `tabItem`
        ),
        ff as(
            select
                nm5,
                nationalpermit,
                concat('National Permit', ' - ', `nationalpermit`, ' ', 'Days to go') as 'NationalPermitCompleteDaysAfter'
            from
                f
            where
                npt >= now() - interval 1 day
                and npt <= now() + interval 30 day
        )

        select
            `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
            InsuranceCompleteDaysAfter!=''
            and (supplier_email = %s or supplier_number=%s)

        union
        select
            `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           FitnessCompleteDaysAfter!=''
           and (supplier_email = %s or supplier_number=%s)

        union
        select
             `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
            PUCCompleteDaysAfter!=''
            and (supplier_email = %s or supplier_number=%s)

        union
        select
             `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
            MVTaxCompleteDaysAfter as 'Completion Date',
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           MVTaxCompleteDaysAfter!=''
           and (supplier_email = %s or supplier_number=%s)

        union
        select
            `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
            ee.StatePermitCompleteDaysAfter as 'Completion Date',
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           StatePermitCompleteDaysAfter!=''
           and (supplier_email = %s or supplier_number=%s)

        union
        select
             `tabItem`.equipment_main_category,
            `tabItem`.register_no,
            `tabItem`.insurance_date,
            `tabItem`.fitness_dt,
            `tabItem`.pollution,
            `tabItem`.mv_tax_upto,
            permit_validity_upto,
            npermit_upto,
            NationalPermitCompleteDaysAfter as 'Completion Date',
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
            left join dd on `tabItem`.name = nm3
            left join ee on `tabItem`.name = nm4
            left join ff on `tabItem`.name = nm5
        where
           NationalPermitCompleteDaysAfter!=''
                 and (supplier_email = %s or supplier_number=%s)


            """, (user, mobile_number, user, mobile_number, user, mobile_number, user, mobile_number, user, mobile_number, user, mobile_number)
        )
        # print(query)
        return query
