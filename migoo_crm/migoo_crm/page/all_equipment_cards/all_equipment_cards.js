frappe.pages['all-equipment-cards'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Equipment Sub Categories',
		single_column: true
	});

	var div = $('<div id="numbercard" class="">\
		<div class="row">\
		</div>\
	</div>');
	page.main.append(div);
	getEquipments()

}

function getEquipments() {

	var urlParams = new URLSearchParams(window.location.search);
	var mainCategory = urlParams.get('item_group');

	frappe.call({
		method: 'migoo_crm.migoo_crm.page.all_equipment_cards.all_equipment_cards.AllEquipments',

		args: {
			main_category: mainCategory,
			supplier_email: frappe.session.user
		},

		callback: function (data) {
			var rows = '';
			var sub_category = data.message[0]

			var length = sub_category.length
			for (var i = 0; i < length; i++) {

				var subCategories = sub_category[i].subCategory

				var totalnumber = sub_category[i].Totalss

				var main_category = sub_category[i].item_group

				if (totalnumber === 0) {
					totalnumber = '<a class="add-equipment" >+ Add Equipment</a>';
				}
				else {
					totalnumber = totalnumber
				}
				rows +=
					''
					+ '<div class="col-md-4">'
					+ '<div class="card-1 row">'

					+ '<div class="title" id="title"> '
					+ (subCategories ? subCategories : '')
					+ '</div>'

					+ '<div class="numbers">'
					+ (totalnumber ? totalnumber : 0)
					+ '</div>'

					+ '<div class="maincategory" hidden id="MainCategory">'
					+ (main_category ? main_category : '')
					+ '</div>'

					+ '</div>'
					+ '</div>'
					;
			}

			$('#numbercard div').html(rows)

			$('.card-1').on('click', function () {

				var parentCategory = $('#MainCategory').text().trim();
				var totalEquipment = parseInt($(this).find('.numbers').text().trim());
				if (totalEquipment > 0) {

					var filter = {
						'item_group': parentCategory,
						'equipment_main_category': $(this).find('.title').text().trim(),
					};

					var filter_string = $.param(filter); // converts filter object to query string
					window.location.href = '/app/item?' + filter_string;
				}

				else {
					$('.add-equipment').on('click', function () {
						var filter = {
							'item_group': parentCategory,
							'equipment_main_category': $(this).closest('.card-1').find('.title').text().trim(),
						}

						var filter_string = $.param(filter); // converts filter object to query string
						window.location.href = '/app/item/new-item-1?' + filter_string;
					});
				}
			});
		}
	})
}
