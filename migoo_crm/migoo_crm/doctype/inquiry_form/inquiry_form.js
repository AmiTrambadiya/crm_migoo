// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inquiry Form', {
	onload: function (frm) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Sales Person",
                fieldname: "sales_person_name",
                filters: { "user_id": frappe.session.user }
            },
            callback: function (r) {
                var sales_person_name = r.message.sales_person_name;
                // Set the sales person field in the Lead form
                if (sales_person_name) {
                    frm.set_value("sales_person", sales_person_name);
                }
            }
        });
    }
});
