// Copyright (c) 2023, Palak Padalia and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Work Summary"] = {
  filters: [
    {
      fieldname: "from_date",
      label: "From Date",
      fieldtype: "Date",
    },
    {
      fieldname: "to_date",
      label: "To Date",
      fieldtype: "Date",
    },
  ],
};
