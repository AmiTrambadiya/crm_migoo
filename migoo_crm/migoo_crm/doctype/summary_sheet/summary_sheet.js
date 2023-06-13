// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Summary Sheet", {
  refresh: function (frm) {
    var element = document.querySelectorAll(".form-section")[2];
    element.classList.add("section-no");
    set_css_1(frm);
    if (frappe.user.has_role("Vendor") === true) {
      if (frm.doc.supplier_approve != null) {
        frm.set_df_property("approve", "hidden", 1);
        frm.set_df_property("reject", "hidden", 1);
      }
    }
    if (frappe.user.has_role("Customer") === true) {
      if (frm.doc.customer_approve != "") {
        frm.set_df_property("approve", "hidden", 1);
        frm.set_df_property("reject", "hidden", 1);
      }
    }

    frm.add_custom_button(__("Get Log Sheet"), function () {
      // alert("HElli")
      let d = new frappe.ui.Dialog({
        title: __("Get Log Sheet"),
        fields: [
          {
            label: __("From"),
            fieldname: "from_time",
            fieldtype: "Date",
            reqd: 1,
            default: frm.doc.resource_planning_start_date,
          },
          {
            label: __("Equipment"),
            fieldname: "equipment",
            fieldtype: "Link",
            options: "Item",
            reqd: 1,
            default: frm.doc.equipment,
          },
          {
            fieldtype: "Column Break",
            fieldname: "col_break_1",
          },
          {
            label: __("To"),
            fieldname: "to_time",
            fieldtype: "Date",
            reqd: 1,
            default: frm.doc.resource_planning_end_date,
          },
          {
            label: __("Customer"),
            fieldname: "customer",
            fieldtype: "Link",
            options: "Customer",
            reqd: 1,
            default: frm.doc.customer,
          },
        ],
        primary_action: function () {
          const data = d.get_values();
          frm.events.get_sheet_data(frm, data);
          d.hide();
        },

        primary_action_label: __("Get Data"),
      });
      d.show();
    });

    var time = 0.0;
    $.each(frm.doc.log_sheet_details || [], function (i, d) {
      time = time + d.total_working_time;
    });
    $.each(frm.doc.items || [], function (i, d) {
      d.hours = time;
    });
  },
  approve: function (frm) {
    if (frappe.user.has_role("Vendor") === true) {
      frm.set_value("supplier_approve", "Approve");
      frm.set_df_property("reject", "hidden", 1);
      frm.save();
    }
    if (frappe.user.has_role("Customer") === true) {
      frm.set_value("customer_approve", "Approve");
      frm.set_df_property("reject", "hidden", 1);
      frm.save();
    }
  },
  reject: function (frm) {
    if (frappe.user.has_role("Vendor") === true) {
      frm.set_value("supplier_approve", "Reject");
      frm.set_df_property("approve", "hidden", 1);
      frm.save();
    }
    if (frappe.user.has_role("Customer") === true) {
      frm.set_value("customer_approve", "Reject");
      frm.set_df_property("approve", "hidden", 1);
      frm.save();
    }
  },
  get_sheet_data(frm, data) {
    // alert("check")
    frappe
      .call({
        method:
          "migoo_crm.migoo_crm.doctype.summary_sheet.summary_sheet.get_logsheet_data",
        args: {
          name: frm.doc.name,
          from_time: data.from_time,
          to_time: data.to_time,
          equipment: data.equipment,
          customer: data.customer,
        },
      })
      .then((r) => {
        //  window.location.reload()

        frm.set_value("total_working_time", r.message["total_working_time"]);
        frm.set_value(
          "overtime_calculation",
          r.message["overtime_calculation"]
        );
        frm.set_value("total_ideal_time", r.message["total_ideal_time"]);
        frm.set_value(
          "total_breckdown_time",
          r.message["total_breckdown_time"]
        );
        frm.set_value("total_time", r.message["total_time"]);
        frm.set_value("total_km", r.message["total_km"]);
        frm.set_value("total_hours", r.message["total_hours"]);
        frm.set_value("total_fuel", r.message["total_fuel"]);
        frm.set_value("start_date", data.from_time);
        frm.set_value("end_date", data.to_time);
      });
    frappe.call({
      method: "frappe.client.get_value",
      args: {
        doctype: "Sales Order",
        fieldname: "working_hours_per_month",
        filters: { name: frm.doc.agreement },
      },
      callback: function (r) {
        var working_hours_per_month = r.message.working_hours_per_month;
        console.log("working_hours_per_month");
        console.log(working_hours_per_month);
        console.log(r);
        frappe.call({
          method:
            "migoo_crm.migoo_crm.doctype.summary_sheet.summary_sheet.get_rate",
          args: {
            parent: frm.doc.agreement,
            item_code: frm.doc.equipment,
          },
          callback: function (r) {
            console.log(r.message);
            var perday = r.message / working_hours_per_month;
            console.log(r.message);
            frm.set_value("rate_per_hours", perday);
            frm.set_value("total_rate", r.message);
            // frm.set_value("total_over_time_price",perday * frm.doc.overtime_calculation)
            // frm.set_value("total_working_price",perday * frm.doc.total_working_time)
            // frm.set_value("total_ideal_price",perday * frm.doc.total_ideal_time)
            // frm.set_value("total_breck_down_price",perday * frm.doc.total_breckdown_time)
          },
        });
        // Set the sales person field in the Lead form
      },
    });
  },
});
function set_css_1(frm) {
  console.log("set_css");
  document.querySelectorAll(
    "[data-fieldname='approve']"
  )[1].style.backgroundColor = "green";
  document.querySelectorAll("[data-fieldname='approve']")[1].style.color =
    "#fff";

  document.querySelectorAll(
    "[data-fieldname='reject']"
  )[1].style.backgroundColor = "red";
  document.querySelectorAll("[data-fieldname='reject']")[1].style.color =
    "#fff";

  // 	document.querySelectorAll("[data-fieldname='fetch_data']")[1].style.marginTop = '25px'
  console.log("End_set_css");
}
