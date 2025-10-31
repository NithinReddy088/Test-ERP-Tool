import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_years

class Employee(Document):
    def validate(self):
        self.validate_dates()
        self.validate_email()
        self.set_employee_number()

    def validate_dates(self):
        if self.date_of_birth and self.date_of_joining:
            if getdate(self.date_of_birth) >= getdate(self.date_of_joining):
                frappe.throw("Date of Birth cannot be greater than or equal to Date of Joining")
            
            # Check minimum age (18 years)
            min_joining_date = add_years(getdate(self.date_of_birth), 18)
            if getdate(self.date_of_joining) < min_joining_date:
                frappe.throw("Employee must be at least 18 years old at the time of joining")

    def validate_email(self):
        if self.personal_email and self.company_email:
            if self.personal_email == self.company_email:
                frappe.throw("Personal Email and Company Email cannot be the same")
        
        # Check for duplicate company email
        if self.company_email:
            existing = frappe.db.get_value("Employee", 
                {"company_email": self.company_email, "name": ["!=", self.name]})
            if existing:
                frappe.throw(f"Company Email {self.company_email} already exists for another employee")

    def set_employee_number(self):
        if not self.employee_number:
            # Auto-generate employee number
            last_emp = frappe.db.sql("""
                SELECT employee_number 
                FROM `tabEmployee` 
                WHERE employee_number IS NOT NULL 
                ORDER BY employee_number DESC 
                LIMIT 1
            """)
            
            if last_emp and last_emp[0][0]:
                try:
                    last_num = int(last_emp[0][0].replace("EMP", ""))
                    self.employee_number = f"EMP{str(last_num + 1).zfill(4)}"
                except:
                    self.employee_number = "EMP0001"
            else:
                self.employee_number = "EMP0001"

    def on_update(self):
        # Create user account if company email is provided
        if self.company_email and not frappe.db.exists("User", self.company_email):
            self.create_user_account()

    def create_user_account(self):
        """Create user account for employee"""
        user = frappe.get_doc({
            "doctype": "User",
            "email": self.company_email,
            "first_name": self.employee_name.split()[0] if self.employee_name else "Employee",
            "last_name": " ".join(self.employee_name.split()[1:]) if len(self.employee_name.split()) > 1 else "",
            "enabled": 1,
            "new_password": "temp123",  # Temporary password
            "roles": [{"role": "Employee"}]
        })
        
        # Add department-specific roles
        if self.department:
            dept_roles = {
                "Manufacturing": ["Manufacturing User"],
                "Quality Control": ["Quality Inspector"],
                "Finance": ["Accounts User"],
                "Sales": ["Sales User"],
                "HR": ["HR User"]
            }
            
            if self.department in dept_roles:
                for role in dept_roles[self.department]:
                    user.append("roles", {"role": role})
        
        user.insert(ignore_permissions=True)
        frappe.msgprint(f"User account created for {self.employee_name} with email {self.company_email}")

@frappe.whitelist()
def get_employee_by_user(user_email):
    """Get employee details by user email"""
    return frappe.get_value("Employee", 
        {"company_email": user_email}, 
        ["name", "employee_name", "department", "designation"], as_dict=True)

@frappe.whitelist()
def get_department_employees(department):
    """Get all employees in a department"""
    return frappe.get_all("Employee",
        filters={"department": department, "status": "Active"},
        fields=["name", "employee_name", "designation", "date_of_joining"])

@frappe.whitelist()
def update_employee_status(employee, status):
    """Update employee status"""
    emp = frappe.get_doc("Employee", employee)
    emp.status = status
    emp.save()
    
    # Disable user account if employee is inactive
    if status in ["Inactive", "Left"] and emp.company_email:
        user = frappe.get_doc("User", emp.company_email)
        user.enabled = 0
        user.save()
    
    return {"status": "success", "message": f"Employee status updated to {status}"}