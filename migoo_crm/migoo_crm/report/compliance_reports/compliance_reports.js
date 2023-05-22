frappe.query_reports["Compliance Reports"] = {
	"filters": [
		// {
		// 	"fieldname": "from_date",
		// 	"label": __("From Date"),
		// 	"fieldtype": "Date",
		// 	"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		// 	"reqd": 1
		// },
		// {
		// 	"fieldname": "to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
		// 	"default": frappe.datetime.get_today(),
		// 	"reqd": 1
		// },
	]
};

$(document).on("click", function (event) {
	if ($(event.target).attr("class").includes('compliance-custom-event')) {
		var test = frappe.new_doc('Compliance Update');
		if (test) {
			localStorage.removeItem("equipment")
			localStorage.setItem("equipment", $(event.target).attr('data-name'))

		}
	}
})
