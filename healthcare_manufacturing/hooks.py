from . import __version__ as app_version

app_name = "healthcare_manufacturing"
app_title = "Healthcare Manufacturing"
app_publisher = "Healthcare ERP"
app_description = "ERP System for Healthcare Equipment Production & Distribution"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "admin@healthcare-erp.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/healthcare_manufacturing/css/healthcare_manufacturing.css"
# app_include_js = "/assets/healthcare_manufacturing/js/healthcare_manufacturing.js"

# include js, css files in header of web template
# web_include_css = "/assets/healthcare_manufacturing/css/healthcare_manufacturing.css"
# web_include_js = "/assets/healthcare_manufacturing/js/healthcare_manufacturing.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "healthcare_manufacturing/public/scss/website"

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

# Installation
# ------------

# before_install = "healthcare_manufacturing.install.before_install"
# after_install = "healthcare_manufacturing.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "healthcare_manufacturing.notifications.get_notification_config"

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

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Order": {
        "on_submit": "healthcare_manufacturing.manufacturing.doctype.production_plan.production_plan.create_production_plan_from_sales_order"
    },
    "Purchase Receipt": {
        "on_submit": "healthcare_manufacturing.quality_control.doctype.quality_inspection.quality_inspection.create_quality_inspection"
    },
    "Work Order": {
        "on_submit": "healthcare_manufacturing.manufacturing.doctype.work_order.work_order.reserve_materials"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "healthcare_manufacturing.manufacturing.doctype.production_plan.production_plan.update_production_schedules"
    ],
    "hourly": [
        "healthcare_manufacturing.inventory.doctype.stock_balance.stock_balance.update_stock_balances"
    ]
}

# Testing
# -------

# before_tests = "healthcare_manufacturing.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "healthcare_manufacturing.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "healthcare_manufacturing.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"healthcare_manufacturing.auth.validate"
# ]