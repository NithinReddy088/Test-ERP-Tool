// Advanced Dashboards with Frappe Charts
frappe.provide('healthcare_manufacturing.dashboards');

healthcare_manufacturing.dashboards = {
    
    // Production Manager Dashboard
    production_dashboard: function(wrapper) {
        const dashboard_html = `
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h2>Production Manager Dashboard</h2>
                    <button class="btn btn-primary btn-sm" onclick="healthcare_manufacturing.dashboards.refresh_production()">
                        Refresh
                    </button>
                </div>
                
                <div class="row dashboard-cards">
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-primary" id="open-work-orders">0</h3>
                                <p>Open Work Orders</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-success" id="completed-today">0</h3>
                                <p>Completed Today</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-warning" id="overdue-orders">0</h3>
                                <p>Overdue Orders</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-info" id="oee-percentage">0%</h3>
                                <p>OEE This Month</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Production Trend</div>
                            <div class="card-body">
                                <div id="production-trend-chart"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Work Order Status</div>
                            <div class="card-body">
                                <div id="work-order-status-chart"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">Upcoming Operations</div>
                            <div class="card-body">
                                <div id="upcoming-operations-table"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $(wrapper).html(dashboard_html);
        this.load_production_data();
    },
    
    // Quality Control Manager Dashboard
    quality_dashboard: function(wrapper) {
        const dashboard_html = `
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h2>Quality Control Dashboard</h2>
                    <button class="btn btn-primary btn-sm" onclick="healthcare_manufacturing.dashboards.refresh_quality()">
                        Refresh
                    </button>
                </div>
                
                <div class="row dashboard-cards">
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-primary" id="pending-inspections">0</h3>
                                <p>Pending Inspections</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-danger" id="open-ncrs">0</h3>
                                <p>Open NCRs</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-success" id="pass-rate">0%</h3>
                                <p>Pass Rate (This Month)</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-warning" id="capa-actions">0</h3>
                                <p>CAPA Actions</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Quality Trend</div>
                            <div class="card-body">
                                <div id="quality-trend-chart"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Defect Categories</div>
                            <div class="card-body">
                                <div id="defect-categories-chart"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">Recent Quality Issues</div>
                            <div class="card-body">
                                <div id="quality-issues-table"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $(wrapper).html(dashboard_html);
        this.load_quality_data();
    },
    
    // Finance Dashboard
    finance_dashboard: function(wrapper) {
        const dashboard_html = `
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h2>Finance Dashboard</h2>
                    <button class="btn btn-primary btn-sm" onclick="healthcare_manufacturing.dashboards.refresh_finance()">
                        Refresh
                    </button>
                </div>
                
                <div class="row dashboard-cards">
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-success" id="monthly-revenue">$0</h3>
                                <p>Monthly Revenue</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-primary" id="accounts-receivable">$0</h3>
                                <p>Accounts Receivable</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-warning" id="accounts-payable">$0</h3>
                                <p>Accounts Payable</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-info" id="profit-margin">0%</h3>
                                <p>Profit Margin</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-8">
                        <div class="card">
                            <div class="card-header">Revenue Trend</div>
                            <div class="card-body">
                                <div id="revenue-trend-chart"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">P&L Summary</div>
                            <div class="card-body">
                                <div id="pl-summary-chart"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">AR Aging</div>
                            <div class="card-body">
                                <div id="ar-aging-table"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">Top Customers</div>
                            <div class="card-body">
                                <div id="top-customers-table"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $(wrapper).html(dashboard_html);
        this.load_finance_data();
    },
    
    load_production_data: function() {
        // Load production metrics
        frappe.call({
            method: 'healthcare_manufacturing.api.analytics.get_production_metrics',
            callback: function(r) {
                if (r.message) {
                    const data = r.message;
                    $('#open-work-orders').text(data.open_work_orders || 0);
                    $('#completed-today').text(data.completed_today || 0);
                    $('#overdue-orders').text(data.overdue_orders || 0);
                    $('#oee-percentage').text((data.oee_percentage || 0) + '%');
                    
                    // Production trend chart
                    new frappe.Chart('#production-trend-chart', {
                        title: 'Daily Production',
                        data: data.production_trend || {
                            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                            datasets: [{
                                name: 'Units Produced',
                                values: [12, 15, 8, 20, 18, 10, 14]
                            }]
                        },
                        type: 'line',
                        height: 250,
                        colors: ['#7cd6fd']
                    });
                    
                    // Work order status chart
                    new frappe.Chart('#work-order-status-chart', {
                        title: 'Work Order Status',
                        data: data.work_order_status || {
                            labels: ['Not Started', 'In Process', 'Completed', 'Stopped'],
                            datasets: [{
                                values: [5, 8, 12, 2]
                            }]
                        },
                        type: 'pie',
                        height: 250,
                        colors: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24']
                    });
                }
            }
        });
    },
    
    load_quality_data: function() {
        // Load quality metrics
        frappe.call({
            method: 'healthcare_manufacturing.api.analytics.get_quality_metrics',
            callback: function(r) {
                if (r.message) {
                    const data = r.message;
                    $('#pending-inspections').text(data.pending_inspections || 0);
                    $('#open-ncrs').text(data.open_ncrs || 0);
                    $('#pass-rate').text((data.pass_rate || 0) + '%');
                    $('#capa-actions').text(data.capa_actions || 0);
                    
                    // Quality trend chart
                    new frappe.Chart('#quality-trend-chart', {
                        title: 'Quality Pass Rate',
                        data: data.quality_trend || {
                            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                            datasets: [{
                                name: 'Pass Rate %',
                                values: [95, 97, 94, 98]
                            }]
                        },
                        type: 'line',
                        height: 250,
                        colors: ['#26de81']
                    });
                    
                    // Defect categories chart
                    new frappe.Chart('#defect-categories-chart', {
                        title: 'Defect Categories',
                        data: data.defect_categories || {
                            labels: ['Dimensional', 'Visual', 'Functional', 'Other'],
                            datasets: [{
                                values: [3, 2, 1, 1]
                            }]
                        },
                        type: 'bar',
                        height: 250,
                        colors: ['#ff9ff3', '#f368e0', '#ff3838', '#ff9f43']
                    });
                }
            }
        });
    },
    
    load_finance_data: function() {
        // Load finance metrics
        frappe.call({
            method: 'healthcare_manufacturing.api.analytics.get_finance_metrics',
            callback: function(r) {
                if (r.message) {
                    const data = r.message;
                    $('#monthly-revenue').text('$' + (data.monthly_revenue || 0).toLocaleString());
                    $('#accounts-receivable').text('$' + (data.accounts_receivable || 0).toLocaleString());
                    $('#accounts-payable').text('$' + (data.accounts_payable || 0).toLocaleString());
                    $('#profit-margin').text((data.profit_margin || 0) + '%');
                    
                    // Revenue trend chart
                    new frappe.Chart('#revenue-trend-chart', {
                        title: 'Monthly Revenue',
                        data: data.revenue_trend || {
                            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                            datasets: [{
                                name: 'Revenue',
                                values: [120000, 135000, 148000, 162000, 155000, 170000]
                            }]
                        },
                        type: 'line',
                        height: 250,
                        colors: ['#2ed573']
                    });
                }
            }
        });
    },
    
    refresh_production: function() {
        this.load_production_data();
    },
    
    refresh_quality: function() {
        this.load_quality_data();
    },
    
    refresh_finance: function() {
        this.load_finance_data();
    }
};