// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Planning', {
	end_date:function(frm){	    
	    if(frm.doc.end_date < frm.doc.start_date)
	    {
	        alert("please enter valid date");
	        return false;
	    }
	    else if(frm.doc.end_date == frm.doc.start_date)
	    {
	        frm.set_value('total_days',frappe.datetime.get_day_diff(frm.doc.end_date ,frm.doc.start_date ))
	       //alert("please enter valid date");
	    }
	    else
	    {
	   //  var totaldays = frappe.datetime.get_day_diff(frm.doc.end_date ,frm.doc.start_date )
	    frm.set_value('total_days',frappe.datetime.get_day_diff(frm.doc.end_date ,frm.doc.start_date ))
	   // alert(frm.doc.total_days)
	    }
	},
	sales_order:function(frm){
	  
	    var order=cur_frm.doc.sales_order;
	    frappe.call({
            method:"order",
            args:{
                "name":order,
            }
	    }).then(records => {
	       // alert(r.data)
	        var a=records["data"]
	       // alert(typeof(a))
	        frm.set_query('equipment', function(doc, cdt, cdn) {
            let d = locals[cdt][cdn];
            return{
				filters: {
				    'item_code': [ 'in',a]
				    
				}
            };
	    });
	    });

	}
});
