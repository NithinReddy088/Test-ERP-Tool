import frappe
from frappe.model.document import Document

class Account(Document):
    def validate(self):
        self.validate_account_name()
        self.validate_parent_account()
        self.set_account_number()

    def validate_account_name(self):
        if not self.account_name:
            frappe.throw("Account Name is required")
        
        # Check for duplicate account names within the same company
        existing = frappe.db.get_value("Account", 
            {"account_name": self.account_name, "company": self.company, "name": ["!=", self.name]})
        if existing:
            frappe.throw(f"Account {self.account_name} already exists for company {self.company}")

    def validate_parent_account(self):
        if self.parent_account:
            parent = frappe.get_doc("Account", self.parent_account)
            if not parent.is_group:
                frappe.throw("Parent Account must be a Group Account")
            
            # Inherit account type from parent if not set
            if not self.account_type:
                self.account_type = parent.account_type

    def set_account_number(self):
        if not self.account_number:
            # Auto-generate account number based on type
            account_type_codes = {
                "Asset": "1",
                "Liability": "2", 
                "Equity": "3",
                "Income": "4",
                "Expense": "5"
            }
            
            type_code = account_type_codes.get(self.account_type, "9")
            
            # Get next number for this type
            last_account = frappe.db.sql("""
                SELECT account_number 
                FROM `tabAccount` 
                WHERE account_number LIKE %s 
                ORDER BY account_number DESC 
                LIMIT 1
            """, f"{type_code}%")
            
            if last_account:
                last_num = int(last_account[0][0][1:]) if len(last_account[0][0]) > 1 else 0
                self.account_number = f"{type_code}{str(last_num + 1).zfill(3)}"
            else:
                self.account_number = f"{type_code}001"

    def update_balance(self, amount, debit_credit="Debit"):
        """Update account balance"""
        if debit_credit == "Debit":
            if self.account_type in ["Asset", "Expense"]:
                self.balance = (self.balance or 0) + amount
            else:
                self.balance = (self.balance or 0) - amount
        else:  # Credit
            if self.account_type in ["Liability", "Equity", "Income"]:
                self.balance = (self.balance or 0) + amount
            else:
                self.balance = (self.balance or 0) - amount
        
        self.save()

@frappe.whitelist()
def get_account_balance(account_name, company):
    """Get current account balance"""
    return frappe.db.get_value("Account", 
        {"account_name": account_name, "company": company}, "balance") or 0

@frappe.whitelist()
def get_chart_of_accounts(company):
    """Get hierarchical chart of accounts"""
    accounts = frappe.get_all("Account",
        filters={"company": company},
        fields=["name", "account_name", "account_type", "parent_account", "is_group", "balance"],
        order_by="account_number")
    
    # Build hierarchy
    account_tree = {}
    for account in accounts:
        if not account.parent_account:
            account_tree[account.name] = account
            account_tree[account.name]["children"] = []
    
    # Add child accounts
    for account in accounts:
        if account.parent_account and account.parent_account in account_tree:
            account_tree[account.parent_account]["children"].append(account)
    
    return list(account_tree.values())