frappe.pages['child-sub-categories'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Child Sub Categories',
		single_column: true
	});
}