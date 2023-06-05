import frappe
from frappe.utils import now_datetime, add_days
from collections import defaultdict


@frappe.whitelist()
def send_insurance_email():

    expiry_date = add_days(now_datetime().date(), 7)

    name = frappe.db.sql("""

    with insurance as(select 
        name,
        supplier,
        supplier_email,
        supplier_name,
        equipment_main_category,
        register_no,
        model,
        insurance_date as 'insurance_dt',
        DATEDIFF(insurance_date, CURDATE()) as 'insuranceDaysToGo',
        CONCAT('Insurance') AS 'insurances'
        from tabItem
        where
        insurance_date >= CURDATE() 
        AND DATEDIFF(insurance_date, CURDATE()) <= 7),

    fitness as(select 
        name,
        supplier,
        supplier_email,
        supplier_name,
        equipment_main_category,
        register_no,
        model,
        fitness_dt as 'fitness_dt',
        DATEDIFF(fitness_dt, CURDATE()) as 'FitnessDaysToGo',
        CONCAT('Fitness') AS 'fitnesses'
        from tabItem
        where
        fitness_dt >= CURDATE() 
        AND DATEDIFF(fitness_dt, CURDATE()) <= 7),

    PUC as(select 
        name,
        supplier,
        supplier_email,
        supplier_name,
        equipment_main_category,
        register_no,
        model,
        pollution as 'pollution_dt',
        DATEDIFF(pollution, CURDATE()) as 'PollutionDaysToGo',
        CONCAT('Pollution') AS 'Pollutions'
        from tabItem
        where
        pollution >= CURDATE()
        AND DATEDIFF(pollution, CURDATE()) <= 7)

    select 
        name,
        supplier,
        supplier_email,
        supplier_name,
        equipment_main_category,
        register_no,
        model,
        DATE_FORMAT(insurance_dt, '%d-%m-%Y'), 
        insurances,
        insuranceDaysToGo

        from insurance

        union

        select 
        name,
        supplier,
        supplier_email,
        supplier_name,
        equipment_main_category,
        register_no,
        model,
        DATE_FORMAT(fitness_dt, '%d-%m-%Y'), 
        fitnesses,
        FitnessDaysToGo
        from fitness

        union

        select 
        name,
        supplier,
        supplier_email,
        supplier_name,
        equipment_main_category,
        register_no,
        model,
        DATE_FORMAT(pollution_dt, '%d-%m-%Y'),
        Pollutions,
        PollutionDaysToGo
        from PUC
    """)

   # create a dictionary to store equipment information for each supplier
    supplier_dict = defaultdict(list)

    for i in name:
        equipment_name = i[0]
        supplier = i[1]
        supplier_email = i[2]
        supplier_name = i[3]
        equipment_main_category = i[4]
        register_no = i[5]
        model = i[6]
        date = i[7]
        status = i[8]
        daystogo = i[9]

        # add equipment information to supplier dictionary
        supplier_dict[supplier].append({
            'equipment_name': equipment_name,
            'supplier_email': supplier_email,
            'supplier_name': supplier_name,
            'equipment_main_category': equipment_main_category,
            'register_no': register_no,
            'model': model,
            'date': date,
            'status': status,
            'daystogo': daystogo
        })

    # loop through supplier dictionary and send a single email to each supplier
    for supplier, equipment_list in supplier_dict.items():
        message = '''
            <div>
                <div class="sec-2">
                    <h3 style="">Hello, {}</h4>
                    <p>We hope this email finds you well. We are writing to remind you that your Equipment's documents are set to expire. The details are mentioned below.</p>
                    <table border=1px cellspacing="0" cellpadding="4";>
                        <tr style="background-color: #e6992a;">
                            <th>Compliance</th>
                            <th>Valid Till</th>
                            <th>Expiring in</th>
                            <th>Equipment</th>
                            <th>Equipment No</th>
                            <th>Model No</th>
                        </tr>
            '''.format(supplier_dict[supplier][0]['supplier_name'])

        # add equipment information for the current supplier to the email message
        for equipment in equipment_list:
            message += '''
                        <tr>
                            <td style="text-align: center;">{}</td>
                            <td style="text-align: center;">{}</td>
                            <td style="text-align: center;">{} Days to Go</td>
                            <td style="text-align: center;">{}</td>
                            <td style="text-align: center;">{}</td>
                            <td style="text-align: center;">{}</td>
                        </tr>
            '''.format(equipment['status'], equipment['date'], equipment['daystogo'], equipment['equipment_main_category'], equipment['register_no'],
                       equipment['model'])
        message += '''
                    </table>
                </div>
            </div>
            <p>Get it renewed as soon as possible to avoid further inconvenience.</p>
            <p>Thank you for choosing Migoo. We value your trust and are committed to providing you with the best service possible.</p>
            <div>
                <table>
                    <tr>
                        <td style="border-right: 2.5px solid #e6992a; ">
                            <img
                                src="https://ci3.googleusercontent.com/mail-sig/AIorK4zf_Mw4U0lrUBfnOuVQzvYfOGDhx1WSRbMtBaWBErGIoq8nQyLPAziA9SF9qRoUVfH4b4fWMfM">
                        </td>
                        <td style="padding-left:12px; color: black;">
                            <div style="display: flex; margin-bottom: 2px;">
                                <img src="https://www.migoo.in/files/call (1).png" height="16px" width="16px"
                                    style="margin-top: auto; margin-bottom: auto;">
                                <div style="margin-left: 5px;">
                                    +91 79692 12202
                                </div>
                            </div>

                            <div style="display: flex; margin-bottom: 2px;">
                                <img src="https://www.migoo.in/files/email1ead26.png" height="16px" width="16px"
                                    style="margin-top: auto; margin-bottom: auto;">
                                <a style="color: black;" href="mailto:surya@migoo.in" style="text-decoration: none;">
                                    <div style="margin-left: 5px;">surya@migoo.in</div>
                                </a>
                            </div>

                            <div style="display: flex; margin-bottom: 2px;">
                                <img src="https://www.migoo.in/files/link.png" height="16px" width="16px"
                                    style="margin-top: auto; margin-bottom: auto;">
                                <a style="color: black;" href="https://www.migoo.in">
                                    <div style="margin-left: 5px;">www.migoo.in</div>
                                </a>
                            </div>

                            <div style="display: flex; margin-bottom: 2px;">
                                <img src="https://www.migoo.in/files/location.png" height="16px" width="16px"
                                    style="margin-top: auto; margin-bottom: auto;">
                                <div style="margin-left: 5px;">Migved Solutions Private Limited,</div>
                            </div>
                            <div style="margin-left: 20px;">
                                A-1204, Mondeal Heights,
                                <br> Iskcon Cross Road, S.G.Highway, <br>
                                Ahmedabad-380058
                            </div>

                            <div style="margin-top: 10px;">
                                <a href="https://www.facebook.com/people/Migoo-Equipments/100087829991875/?mibextid=ZbWKwL"
                                    target="_blank">
                                    <img src="https://www.migoo.in/files/facebook.png" style="height: 20px;"></a>

                                <a href="https://www.instagram.com/migoo_equipment/?igshid=YmMyMTA2M2Y%3D">
                                    <img src="https://www.migoo.in/files/instagram.png" style="height: 20px;"></a>

                                <a
                                    href="https://www.linkedin.com/authwall?trk=bf&trkInfo=AQE3GrOu_soLXAAAAYTnfV7Ak5NhrLNM9IxIvNuvfFL51XjUZjWDRN_WROWhhGDHQfI05HuUk46hX4INHsRvXff6X08bFwXCpC3OG-A7nocY7Rtqb7kN1teuUQMukrXRVO5ai84=&original_referer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fmigoo-equipments-270563257">
                                    <img src="https://www.migoo.in/files/linkedin.png" style="height: 20px;"></a>

                                <a href="https://twitter.com/MigooEquipments">
                                    <img src="https://www.migoo.in/files/twitter-sign.png" style="height: 20px;"></a>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>

            <br>
            <div>

                <div style="display: flex; margin-bottom: 2px;">
                    <img
                        src="https://lh4.googleusercontent.com/Tg-ugYQdUjAPJTtdSu3Rc8pYT0hONyb7dbg-Z0LN2iYvKbhazcdWIu_Vyn7-m7IIPdU0fd9VwxdDKm90nE6tVaAeQ4_b13OV79O7w9sPJiJP4YOqt2juD4XWgjK4v4E5TmIVuOsY3dDyuQ7p3-B4ndw">
                    <div style="color: green; margin-left: 5px;">Consider The Environment. Think Before You Print.</div>
                </div>
            </div>
            '''

        frappe.sendmail(
            recipients=[supplier_dict[supplier][0]['supplier_email']],
            subject='Important Notice: Renewal Remainders of Equipment', message=message)
