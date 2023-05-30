frappe.pages['equipment'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Equipment Dashboard',
		single_column: true
	});

	var div = $('<div id="numbercard" class="">\
		<div class="row">\
		</div>\
		</div><div id="po-message"></div>');

	var canvas = $('<br><h3>Equipment Status</h3><br><div id="chart"></div><div id="po-message1"></div>');
	var br = $('<br><br><h3>Compliance Report</h3><br>')

	page.main.append(div);
	page.main.append(canvas);
	page.main.append(br);

	var table_wrapper = $('<div>').attr('id', 'my_report_table').addClass('').appendTo(page.main);
	var table_message = $('<div>').attr('id', 'po-message2').addClass('').appendTo(page.main);


	getNumberCards()
	getDashboardChart()
	getGridReport()
}

function getNumberCards() {

	frappe.call({
		method: 'migoo_crm.migoo_crm.page.equipment.equipment.equipment',

		args: {
			filters: {
				owner: frappe.session.user
			},
		},

		callback: function (data) {
			var rows = '';

			if (data.message.length === 0) {
				$('#po-message').html('<div class="">\
				<img class="img-nothing" src="/files/list-empty-state.svg">\
				<div class= "image-text">\
				Nothing To Show\
				</div>\
				</div>');
			}

			else {
				$('#po-message').hide();

				$.each(data.message, function (i, d) {

					var TotalNoOfequipment = d.TotalEquipment

					if (TotalNoOfequipment === 0) {
						TotalNoOfequipment = '<a class="add-equipment" >+ Add Equipment</a>';
					}
					else {
						TotalNoOfequipment = TotalNoOfequipment
					}

					rows +=
						''
						+ '<div class="col-md-6 col-lg-4 col-sm-12">'
						+ '<div class="card-1 row">'

						+ '<div class="col-lg-8 col-md-9 col-sm-9">'
						+ '<div class="title">'
						+ (d.ItemGroup ? d.ItemGroup : '')
						+ '</div>'

						+ '<div class="numbers">'
						+ (TotalNoOfequipment ? TotalNoOfequipment : 0)
						+ '</div>'
						+ '</div>'

						+ '<div class="col-lg-4 col-md-3 col-sm-3">'
						+ '<div class="title">'
						+ '<img  src="'
						+ (d.Image ? d.Image : '')
						+ '">'
						+ '</div>'
						+ '</div>'

						+ '</div>'
						+ '</div>'
						;
				});

				$('#numbercard div').html(rows)

				$('.card-1').on('click', function () {
					var totalEquipment = parseInt($(this).find('.numbers').text().trim());

					if (totalEquipment > 0) {
						var filter = {
							'item_group': $(this).find('.title').text().trim()
						};

						var filter_string = $.param(filter); // converts filter object to query string
						window.location.href = 'all-equipment-cards?' + filter_string;
					}

					else {
						$('.add-equipment').on('click', function () {
							var filter = {
								'item_group': $(this).closest('.card-1').find('.title').text().trim()
							};

							var filter_string = $.param(filter); // converts filter object to query string
							window.location.href = '/app/item/new-item-1?' + filter_string;
						});
					}

				});
			}
		}
	})
}

function getDashboardChart() {
	frappe.call({
		method: 'migoo_crm.migoo_crm.page.equipment.equipment.get_equipment_by_category',

		args: {
			filters: {
				owner: frappe.session.user
			},
		},

		callback: function (data) {
			// console.log(data);
			var chart_data = data.message;

			var labels = [];
			var values = [];
			var colorsArray = [];

			if (data.message.length === 0) {
				$('#po-message1').html('<div class="">\
				<img class="img-nothing" src="/files/list-empty-state.svg">\
				<div class= "image-text">\
				Nothing To Show\
				</div>\
				</div>');
			}

			else {
				$('#po-message1').hide();
				chart_data.forEach(function (item) {
					var color = '#' + Math.floor(Math.random() * 16777215).toString(16);
					colorsArray.push(color);
					labels.push(item.label);
					values.push(item.value);
				});

				var chart = new frappe.Chart("#chart", {
					data: {
						labels: labels,
						datasets: [
							{
								type: "bar",
								values: values,
								colors: colorsArray,
							}
						]
					},
					type: 'bar',
					height: 360,
					colors: colorsArray
				});
			}
		}
	});
}

function getGridReport() {

	var col = [
		{
			name: 'Equipment',
			width: 115,
			editable: false,
		},
		{
			name: 'RTO Regsitration No',
			width: 115,
			editable: false,
		},
		{
			name: 'Insurance Last Date',
			width: 115,
			editable: false,
		},
		{
			name: 'Fitness Last Date',
			width: 115,
			editable: false,
		},
		{
			name: 'PUC Last Date',
			width: 115,
			editable: false,
		},
		{
			name: 'MV Tax Last Date',
			width: 115,
			editable: false,
		},
		{
			name: 'State Permit Last Date',
			width: 115,
			editable: false,
		},
		{
			name: 'National Last Date',
			width: 115,
			editable: false,
		},
		{
			name: 'Completion Date',
			width: 115,
			editable: false,
		},
		{
			width: 115,
			editable: false,
		}
	];

	frappe.call({
		method: 'migoo_crm.migoo_crm.page.equipment.equipment.get_compliance_report',
		args: {
			filters: {
				owner: frappe.session.user
			},
		},

		callback: function (response) {

			if (response.message.length === 0) {
				$('#po-message2').html('<div class="">\
				<img class="img-nothing" src="/files/list-empty-state.svg">\
				<div class= "image-text">\
				Nothing To Show\
				</div>\
				</div>');
			}

			else {
				$('#po-message2').hide();
				var data = response.message;
				new DataTable('#my_report_table', {
					columns: col,
					data: data,
				});
			}
		}
	});
}