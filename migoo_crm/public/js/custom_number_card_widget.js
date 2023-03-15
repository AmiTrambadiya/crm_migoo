frappe.provide("frappe.utils");
frappe.provide("frappe.widget");


frappe.widget.widget_factory.number_card.prototype.render_number = function render_number() {
	let custom_current_dashboard_name = ''
	try{
		custom_current_dashboard_name = cur_page.page.page.title
	}catch(e){}
	if(custom_current_dashboard_name === 'Equipment Dashboard'){
		return this.get_number().then(() => {
			let equipment_number = this.formatted_number
			if(equipment_number===0){
				equipment_number = `<span style='color:#687178!important;font-weight:600;font-size:0.77em;'>+ Add Equipment</span>`
				$(this.body).html(`<div class="widget-content">
					<div class="number" style="color:${this.card_doc.color};">${equipment_number}</div>
					</div>`);
			}else{
				$(this.body).html(`<div class="widget-content">
					<div class="number" style="color:${this.card_doc.color};">${equipment_number}</div>
					</div>`);
			}
		});
	}else{
		return this.get_number().then(() => {
			$(this.body).html(`<div class="widget-content">
				<div class="number" style="color:${this.card_doc.color};">${this.formatted_number}</div>
				</div>`);
		});
	}
}

frappe.widget.widget_factory.number_card.prototype.set_route = function set_route() {
	let equipment_form_custom_route = false;
	try{
		equipment_form_custom_route = cur_page.page.page.title ==='Equipment Dashboard' && this.number === 0;
	}catch(e){}
	const is_document_type = this.card_doc.type !== "Report";
	const name = is_document_type ? this.card_doc.document_type : this.card_doc.report_name;
	if(!equipment_form_custom_route){
		const route = frappe.utils.generate_route({
			name: name,
			type: is_document_type ? "doctype" : "report",
			is_query_report: !is_document_type,
		});

		if (is_document_type) {
			const filters = JSON.parse(this.card_doc.filters_json);
			frappe.route_options = filters.reduce((acc, filter) => {
				return Object.assign(acc, {
					[`${filter[0]}.${filter[1]}`]: [filter[2], filter[3]],
				});
			}, {});
		}	
		frappe.set_route(route);
	}else{
		// custom code
		var doc = frappe.model.get_new_doc(name);
		doc.item_group = this.name;
		frappe.set_route('Form',name, doc.name);
		// end custom code
	}
	
}

frappe.widget.widget_factory.number_card.prototype.set_card_actions = function set_card_actions(actions) {
}
frappe.widget.widget_factory.chart.prototype.set_chart_actions=function set_chart_actions(actions){
}