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
        insurance_dt,
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
        fitness_dt,
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
        pollution_dt,
        Pollutions,
        PollutionDaysToGo
        from PUC
    """)

    # return name

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
                    <h4 style="color:#e6992a">Hello, {}</h4>
                    <p>We hope this email finds you well. We are writing to remind you that your Equipment's documents are set to expire. The details are mentioned below.</p>
                    <table border=1px cellspacing="0" cellpadding="0";>
                        <tr>
                            <th>Equipment</th>
                            <th>Equipment No</th>
                            <th>Model No</th>
                            <th>Document Status</th>
                            <th>Date</th>
                            <th>Expiring in</th>
                        </tr>
            '''.format(supplier_dict[supplier][0]['supplier_name'])

        # add equipment information for the current supplier to the email message
        for equipment in equipment_list:
            message += '''
                        <tr>
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                            <td>Insurance</td>
                            <td>{}</td>
                            <td>{} Days to Go</td>
                        </tr>
            '''.format(equipment['equipment_main_category'], equipment['register_no'],
                       equipment['model'], equipment['date'], equipment['daystogo'])

        message += '''
                    </table>
                </div>
            </div>
            <p>Get it renewed as soon as possible to avoid further inconvenience.</p>
            <p>Thank you for choosing Migoo. We value your trust and are committed to providing you with the best service possible.</p>
            <div style="padding-top:10px;">
                 <div>
                <p>Thanks & Regards,</p>
                <img src="https://www.migoo.in/files/download%20(1).png">
                <div>Surya Prakash Pal </div>
                <div>Assistant Manager</div>
                <div>Mobile No.: +917969212202</div>
                <div>Email: mailto:surya@migoo.in</div>
                </div>
                <br>
                <a href="https://www.facebook.com/people/Migoo-Equipments/100087829991875/?mibextid=ZbWKwL">
                    <img src="https://www.migoo.in/files/facebook.png" style="height: 25px;"></a>
    
                <a href="https://www.instagram.com/migoo_equipment/?igshid=YmMyMTA2M2Y%3D">
                    <img src="https://www.migoo.in/files/instagram.png" style="height: 25px;"></a>

                <a href="https://www.linkedin.com/authwall?trk=bf&trkInfo=AQE3GrOu_soLXAAAAYTnfV7Ak5NhrLNM9IxIvNuvfFL51XjUZjWDRN_WROWhhGDHQfI05HuUk46hX4INHsRvXff6X08bFwXCpC3OG-A7nocY7Rtqb7kN1teuUQMukrXRVO5ai84=&original_referer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fmigoo-equipments-270563257">
                    <img src="https://www.migoo.in/files/linkedin.png" style="height: 25px;"></a>

                <a href="https://api.whatsapp.com/send/?phone=917969212200&text&type=phone_number&app_absent=0">
                    <img src="https://www.migoo.in/files/123whatsapp.png" style="height: 25px;"></a>

                <a href="https://twitter.com/MigooEquipments">
                    <img src="https://www.migoo.in/files/twitter-sign.png" style="height: 25px;"></a>
        </div>
            '''

        frappe.sendmail(
            recipients=[supplier_dict[supplier][0]['supplier_email']],
            subject='Important Notice: Renewal Remainders of Equipment', message=message)
