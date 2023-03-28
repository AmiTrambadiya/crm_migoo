

$(document).on("click",function (event){
	if($(event.target).attr("class").includes('compliance-custom-event')){
		var test = frappe.new_doc('Compliance Update');
		if(test)
		{
			localStorage.removeItem("equipment")
			localStorage.setItem("equipment",$(event.target).attr('data-name'))
						
		}
	}	
})

