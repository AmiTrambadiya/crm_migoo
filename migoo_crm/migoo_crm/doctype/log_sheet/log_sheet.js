// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Log Sheet", {
  // refresh: function(frm) {

  // }

  before_save: function (frm) {
    var hours = 0;
    var minutes = 0;
    var seconds = 0;
    var w_total_time = 0;
    var working = 0;
    var ideal = 0;
    var BreckDown = 0;
    var t = 0;
    var tot1 = 0.0;
    var w_h = 0;
    var w_m = 0;
    var i_h = 0;
    var i_m = 0;
    var b_h = 0;
    var b_m = 0;
    var w_tot = 0;
    var i_tot = 0;
    var b_tot = 0;
    var cc = 0.0;
    var tot_hours = 0.0;
    $.each(frm.doc.working_details || [], function (i, d) {
      if (d.status == "Working") {
        var hour1 = d.total_time.split(":")[0];
        var min1 = d.total_time.split(":")[1];
        var w1 = 0;
        w1 = parseInt(hour1);
        // alert(w1);
        var w2 = 0;
        w2 = parseInt(min1);
        w_h = w_h + w1;
        w_m = w_m + w2;
        if (w_m > 60) {
          var min = w_m / 60;

          w_h = w_h + parseInt(min);
          var mmm = parseInt(min) * 60;
          w_m = w_m - parseInt(mmm);
        }
        var w_ot = w_h + "." + w_m;
        w_tot = parseFloat(w_tot) + parseFloat(w_ot);
        frm.set_value("total_working_time", parseFloat(w_tot));
      }
      if (d.status == "Ideal") {
        var hour1 = d.total_time.split(":")[0];
        var min1 = d.total_time.split(":")[1];
        var w1 = 0;
        w1 = parseInt(hour1);
        var w2 = 0;
        w2 = parseInt(min1);
        i_h = i_h + w1;
        i_m = i_m + w2;
        if (i_m > 60) {
          var min = i_m / 60;

          i_h = i_h + parseInt(min);
          var mmm = parseInt(min) * 60;
          i_m = i_m - parseInt(mmm);
        }
        var i_ot = i_h + "." + i_m;
        i_tot = parseFloat(i_tot) + parseFloat(i_ot);
        frm.set_value("total_ideal_time", parseFloat(i_tot));
      }
      if (d.status == "Breakdown") {
        var hour1 = d.total_time.split(":")[0];

        var min1 = d.total_time.split(":")[1];

        var w1 = 0;
        w1 = parseInt(hour1);

        var w2 = 0;
        w2 = parseInt(min1);
        b_h = b_h + w1;
        b_m = b_m + w2;
        if (b_m > 60) {
          var min = b_m / 60;

          b_h = b_h + parseInt(min);
          var mmm = parseInt(min) * 60;
          b_m = b_m - parseInt(mmm);
        }
        var b_ot = b_h + "." + b_m;

        b_tot = parseFloat(b_tot) + parseFloat(b_ot);
        frm.set_value("total_breckdown_time", parseFloat(b_tot));
      }
      // frm.set_value("total_time",)
      var total = d.total_km;
      t = t + total;
      frm.set_value("total_km", t);

      tot_hours = tot_hours + d.total_hours;
      frm.set_value("total_hours", tot_hours);
    });
    var aa = frm.doc.total_ideal_time;
    var bb = frm.doc.total_working_time;
    if (bb > frm.doc.working_hours_per_day) {
      // alert(frm.doc.working_hours_per_day)
      var tt = bb - frm.doc.working_hours_per_day;
      frm.set_value("overtime_calculation", tt);
    }
    //  alert(typeof(bb))
    var cc = parseFloat(aa) + parseFloat(bb);
    // frm.set_value("total_km",cc)
    // alert(typeof(cc))
    frm.set_value("total_time", cc);

    var totalfuel = 0;
    var fueldata = frm.doc.fuel_details || [];
    var length = fueldata.length;
    for (var i = 0; i < fueldata.length; i++) {
      totalfuel += fueldata[i].fuel_lt;
    }

    frm.set_value("total_fuel", totalfuel);
  },
});
frappe.ui.form.on('Working Details', {
	start_time:function(frm) {
	   $.each(frm.doc.working_details || [], function (i, d) {
// 		alert(d.start_time)
        var hours=0; 
        var minutes=0; 
        
        // var seconds=0; 
        if(!(/^\d{1,2}:\d{1,2}$/.test(d.start_time)))
        {
       		alert("Please enter valid time format");
       	   
            d.start_time= "00:00"
        }
        else
        {
             if (d.start_time && d.end_time) 
            { 
                    // alevar ww = 0;
            // var www = 0;rt("if")
                    var hour1 = d.start_time.split(':')[0]; 
                    var hour2 = d.end_time.split(':')[0]; 
                    var min1 = d.start_time.split(':')[1]; 
                    var min2 = d.end_time.split(':')[1]; 
                    // varvar ww = 0;
            // var www = 0; sec1 = d.start_time.split(':')[2]; 
                    // var sec2 = d.end_time.split(':')[2]; 
                    var diff_hour = hour2 - hour1; 
                    var diff_min = min2 - min1; 
                    // var diff_sec = sec2 - sec1; 
                    if (diff_hour<0) 
                    { 
                        diff_hour+= 24; 
              var ww = 0;
            var www = 0;       } 
                    if (diff_min<0) 
                    { 
                        diff_min+=60; 
                        diff_hour--; 
                    }
                    if(diff_min>=60)
                    { 
                        diff_min-=60; 
                        diff_hour++; 
                    } 
                    // if (diff_sec<0) 
                    // { 
                    //     diff_sec+=60; 
                    //     diff_min--; 
                    // } 
                    // else if(diff_sec>=60)
                    // { 
                    //     diff_sec-=60; 
                    //     diff_min++; 
                    // } 
                    d.total_time = diff_hour+":"+diff_min
                    // alert(d.total_time)
                
                    // frappe.model.set_value(cdt,cdn,"total_time",diff_hour+":"+diff_min+":"+diff_sec); 
                    frm.refresh_field("working_details"); 
                } 
        }
		})
	},
	end_time:function(frm) {
	   // alert("rjjt")
		$.each(frm.doc.working_details || [], function (i, d) {
// 		alert(d.start_time)
        var hours=0; 
        var minutes=0; 
        var seconds=0; 
        
        
         if(!(/^\d{1,2}:\d{1,2}$/.test(d.end_time)))
        {
       		alert("Please enter valid time format");
       	    d.end_time= "00:00"
        }
        else
        {
            if (d.start_time && d.end_time) 
            { 
                // alert("if")
                var hour1 = d.start_time.split(':')[0]; 
                var hour2 = d.end_time.split(':')[0]; 
                var min1 = d.start_time.split(':')[1]; 
                var min2 = d.end_time.split(':')[1]; 
                // var sec1 = d.start_time.split(':')[2]; 
                // var sec2 = d.end_time.split(':')[2]; 
                var diff_hour = hour2 - hour1; 
                var diff_min = min2 - min1; 
                // var diff_sec = sec2 - sec1; 
                if (diff_hour<0) 
                { 
                    diff_hour+= 24; 
                } 
                if (diff_min<0) 
                { 
                    diff_min+=60; 
                    diff_hour--; 
                }
                if(diff_min>=60)
                { 
                    diff_min-=60; 
                    diff_hour++; 
                } 
                // if (diff_sec<0) 
                // { 
                //     diff_sec+=60; 
                //     diff_min--; 
                // } 
                // else if(diff_sec>=60)
                // { 
                //     diff_sec-=60; 
                //     diff_min++; 
                // } 
                d.total_time = diff_hour+":"+diff_min
                // alert(d.total_time)
            
                // frappe.model.set_value(cdt,cdn,"total_time",diff_hour+":"+diff_min+":"+diff_sec); 
                frm.refresh_field("working_details"); 
            }
        }
		})
	},
	start_km:function(frm) {
	    $.each(frm.doc.working_details || [], function (i, d) {
		var a = d.start_km
		var b = d.end_km
		var c = b - a;
		if(d.end_km!=""){
		if(a>b){
		    alert("Please enter proper values")
		    validated=false
		}
		else{
		d.total_km=c;
		 frm.refresh_field("working_details"); 
		}
		}
	    })
	},
		end_km:function(frm) {
		    $.each(frm.doc.working_details || [], function (i, d) {
		var a = d.start_km
		var b = d.end_km
		var c = b - a;
		
		if(a>b){
		    alert("Please enter proper values")
		    validated=false
		}
		else{
		d.total_km=c;
		 frm.refresh_field("working_details"); 
		
		}
		    })
	},
	start_hours:function(frm)
	{
	     $.each(frm.doc.working_details || [], function (i, d) {
		var a = d.start_hours
		var b = d.end_hours
		var c = b - a;
		if(b!=0.00){
    		if(a>b){
    		    alert("Please enter proper values")
    		    validated=false
    		}
		}
    		else{
    		d.total_hours=c;
    		 frm.refresh_field("working_details"); 
    		
    		}
		
		    })
	},
		end_hours:function(frm)
	{
	     $.each(frm.doc.working_details || [], function (i, d) {
		var a = d.start_hours
		var b = d.end_hours
		var c = b - a;
		
		if(a>b){
		    alert("Please enter proper values")
		    validated=false
		}
		else{
		d.total_hours=c;
		 frm.refresh_field("working_details"); 
		
		}
		    })
	}
	

})