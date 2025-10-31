import frappe
from frappe.model.document import Document
from frappe.utils import flt

class KPI(Document):
    def validate(self):
        self.validate_calculation_method()
        self.validate_sql_query()

    def validate_calculation_method(self):
        if self.calculation_method == "Custom SQL" and not self.sql_query:
            frappe.throw("SQL Query is required for Custom SQL calculation method")

    def validate_sql_query(self):
        if self.sql_query:
            # Basic SQL injection prevention
            dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
            query_upper = self.sql_query.upper()
            
            for keyword in dangerous_keywords:
                if keyword in query_upper:
                    frappe.throw(f"SQL Query cannot contain {keyword} statements")

    def calculate_current_value(self):
        """Calculate current KPI value based on calculation method"""
        try:
            if self.calculation_method == "Custom SQL":
                result = frappe.db.sql(self.sql_query)
                if result and result[0]:
                    self.current_value = flt(result[0][0])
            else:
                # Use predefined calculation methods
                self.current_value = self.get_predefined_calculation()
            
            self.save()
            return self.current_value
            
        except Exception as e:
            frappe.log_error(f"KPI Calculation Error for {self.kpi_name}: {str(e)}")
            return 0

    def get_predefined_calculation(self):
        """Get predefined KPI calculations"""
        kpi_calculations = {
            "Production Efficiency": self.calculate_production_efficiency,
            "Quality Pass Rate": self.calculate_quality_pass_rate,
            "On-Time Delivery": self.calculate_on_time_delivery,
            "Inventory Turnover": self.calculate_inventory_turnover,
            "Customer Satisfaction": self.calculate_customer_satisfaction
        }
        
        if self.kpi_name in kpi_calculations:
            return kpi_calculations[self.kpi_name]()
        
        return 0

    def calculate_production_efficiency(self):
        """Calculate production efficiency percentage"""
        # Get completed work orders vs planned
        completed = frappe.db.count("Work Order", {"status": "Completed"})
        total = frappe.db.count("Work Order", {"status": ["!=", "Cancelled"]})
        
        if total > 0:
            return (completed / total) * 100
        return 0

    def calculate_quality_pass_rate(self):
        """Calculate quality inspection pass rate"""
        passed = frappe.db.count("Quality Inspection", {"status": "Accepted"})
        total = frappe.db.count("Quality Inspection", {"status": ["in", ["Accepted", "Rejected"]]})
        
        if total > 0:
            return (passed / total) * 100
        return 0

    def calculate_on_time_delivery(self):
        """Calculate on-time delivery percentage"""
        # This would need delivery note data in a real implementation
        return 93  # Mock value

    def calculate_inventory_turnover(self):
        """Calculate inventory turnover ratio"""
        # This would need cost of goods sold and average inventory
        return 10  # Mock value

    def calculate_customer_satisfaction(self):
        """Calculate customer satisfaction score"""
        # This would need customer feedback data
        return 4.2  # Mock value

    def get_performance_indicator(self):
        """Get performance indicator based on current vs target value"""
        if not self.target_value or not self.current_value:
            return "neutral"
        
        percentage = (self.current_value / self.target_value) * 100
        
        if percentage >= 100:
            return "excellent"
        elif percentage >= 90:
            return "good"
        elif percentage >= 80:
            return "average"
        else:
            return "poor"

@frappe.whitelist()
def update_all_kpis():
    """Update all active KPIs"""
    kpis = frappe.get_all("KPI", filters={"is_active": 1}, fields=["name"])
    
    updated_count = 0
    for kpi in kpis:
        kpi_doc = frappe.get_doc("KPI", kpi.name)
        kpi_doc.calculate_current_value()
        updated_count += 1
    
    return {"status": "success", "message": f"Updated {updated_count} KPIs"}

@frappe.whitelist()
def get_kpi_dashboard_data():
    """Get KPI data for dashboard display"""
    kpis = frappe.get_all("KPI", 
        filters={"is_active": 1},
        fields=["kpi_name", "kpi_type", "current_value", "target_value", "chart_type", "color"])
    
    dashboard_data = []
    for kpi in kpis:
        kpi_doc = frappe.get_doc("KPI", kpi.kpi_name)
        dashboard_data.append({
            "name": kpi.kpi_name,
            "type": kpi.kpi_type,
            "current_value": kpi.current_value,
            "target_value": kpi.target_value,
            "chart_type": kpi.chart_type,
            "color": kpi.color,
            "performance": kpi_doc.get_performance_indicator()
        })
    
    return dashboard_data

@frappe.whitelist()
def get_kpi_trend_data(kpi_name, period="monthly"):
    """Get KPI trend data for charts"""
    # This would fetch historical KPI values
    # For now, return mock trend data
    mock_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "datasets": [{
            "name": kpi_name,
            "values": [85, 87, 82, 90, 88, 92]
        }]
    }
    
    return mock_data