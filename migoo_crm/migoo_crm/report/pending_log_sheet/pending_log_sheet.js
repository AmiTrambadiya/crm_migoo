// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pending Log Sheet"] = {
  filters: [
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
    },
    {
      fieldname: "equipment_sub_category",
      label: __("Equipment"),
      fieldtype: "Link",
      options: "Item Group",
      get_query: function () {
        return {
          filters: {
            parent_item_group: ["!=", "All Equipment Groups"], // Exclude 'All Equipment Group' parent item group
          },
        };
      },
    },
    {
      fieldname: "name",
      label: __("Equipment Planning"),
      fieldtype: "Link",
      options: "Equipment Planning",
    },
    {
      fieldname: "supplier",
      label: __("Supplier"),
      fieldtype: "Link",
      options: "Supplier",
    },
    {
      fieldname: "driver",
      label: __("Driver"),
      fieldtype: "Link",
      options: "Driver",
    },
    {
      fieldname: "customer",
      label: __("Customer"),
      fieldtype: "Link",
      options: "Customer",
    },
  ],
};
