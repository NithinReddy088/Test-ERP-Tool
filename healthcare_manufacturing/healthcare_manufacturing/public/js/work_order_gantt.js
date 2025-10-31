// Work Order Gantt Chart Implementation
frappe.provide('healthcare_manufacturing.gantt');

healthcare_manufacturing.gantt = {
    init: function(wrapper) {
        this.wrapper = wrapper;
        this.setup_gantt();
    },

    setup_gantt: function() {
        const me = this;
        
        // Fetch work orders data
        frappe.call({
            method: 'healthcare_manufacturing.api.manufacturing.get_production_schedule',
            callback: function(r) {
                if (r.message) {
                    me.render_gantt(r.message);
                }
            }
        });
    },

    render_gantt: function(data) {
        const gantt_html = `
            <div class="gantt-container">
                <div class="gantt-header">
                    <h3>Production Schedule - Gantt View</h3>
                    <button class="btn btn-primary btn-sm" onclick="healthcare_manufacturing.gantt.refresh()">
                        Refresh
                    </button>
                </div>
                <div class="gantt-chart" id="gantt-chart"></div>
            </div>
        `;
        
        $(this.wrapper).html(gantt_html);
        
        // Initialize Gantt chart using Frappe's built-in Gantt
        this.gantt_chart = new frappe.Gantt('#gantt-chart', data, {
            header_height: 50,
            column_width: 30,
            step: 24,
            view_modes: ['Quarter Day', 'Half Day', 'Day', 'Week', 'Month'],
            bar_height: 20,
            bar_corner_radius: 3,
            arrow_curve: 5,
            padding: 18,
            view_mode: 'Day',
            date_format: 'YYYY-MM-DD',
            custom_popup_html: function(task) {
                return `
                    <div class="details-container">
                        <h5>${task.name}</h5>
                        <p>Item: ${task.item}</p>
                        <p>Progress: ${task.progress}%</p>
                        <p>Start: ${task.start}</p>
                        <p>End: ${task.end}</p>
                    </div>
                `;
            },
            on_click: function(task) {
                frappe.set_route('Form', 'Work Order', task.id);
            },
            on_date_change: function(task, start, end) {
                // Update work order dates
                frappe.call({
                    method: 'healthcare_manufacturing.api.manufacturing.update_work_order_dates',
                    args: {
                        work_order: task.id,
                        start_date: start,
                        end_date: end
                    }
                });
            },
            on_progress_change: function(task, progress) {
                // Update work order progress
                frappe.call({
                    method: 'healthcare_manufacturing.api.manufacturing.update_work_order_progress',
                    args: {
                        work_order: task.id,
                        progress: progress
                    }
                });
            }
        });
    },

    refresh: function() {
        this.setup_gantt();
    }
};

// Add to Work Order list view
frappe.listview_settings['Work Order'] = {
    add_fields: ["status", "planned_start_date", "planned_end_date"],
    get_indicator: function(doc) {
        return [__(doc.status), {
            "Draft": "red",
            "Not Started": "orange", 
            "In Process": "blue",
            "Completed": "green",
            "Stopped": "red",
            "Cancelled": "dark grey"
        }[doc.status], "status,=," + doc.status];
    },
    onload: function(listview) {
        listview.page.add_menu_item(__("Gantt View"), function() {
            frappe.route_options = {};
            frappe.set_route("query-report", "Work Order Gantt");
        });
    }
};