from . import __version__ as app_version

app_name = "migoo_crm"
app_title = "Migoo CRM"
app_publisher = "Palak Padalia"
app_description = "MIGOO"
app_email = "padaliapalak19@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/migoo_crm/css/migoo_crm.css"
# app_include_js = "/assets/migoo_crm/js/migoo_crm.js"

# include js, css files in header of web template
# web_include_css = "/assets/migoo_crm/css/migoo_crm.css"
# web_include_js = "/assets/migoo_crm/js/migoo_crm.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "migoo_crm/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "migoo_crm.utils.jinja_methods",
#	"filters": "migoo_crm.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "migoo_crm.install.before_install"
# after_install = "migoo_crm.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "migoo_crm.uninstall.before_uninstall"
# after_uninstall = "migoo_crm.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "migoo_crm.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "User": "migoo_crm.code_override.user.User",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"migoo_crm.tasks.all"
#	],
#	"daily": [
#		"migoo_crm.tasks.daily"
#	],
#	"hourly": [
#		"migoo_crm.tasks.hourly"
#	],
#	"weekly": [
#		"migoo_crm.tasks.weekly"
#	],
#	"monthly": [
#		"migoo_crm.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "migoo_crm.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "frappe.core.doctype.user.user.update_password": "migoo_crm.code_override.user.update_password",
    "erpnext.crm.doctype.lead.lead.make_opportunity": "migoo_crm.code_override.lead.make_opportunity",
    "erpnext.crm.doctype.lead.lead.make_customer": "migoo_crm.code_override.lead.make_customer",
    "erpnext.crm.doctype.opportunity.opportunity.make_customer":"migoo_crm.code_override.opportunity.make_customer"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "migoo_crm.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"migoo_crm.auth.validate"
# ]
