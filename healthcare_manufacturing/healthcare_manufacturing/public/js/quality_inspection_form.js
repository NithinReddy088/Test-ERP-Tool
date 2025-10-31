// Quality Inspection Inline Form with Photo Upload
frappe.ui.form.on('Quality Inspection', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Add Photos'), function() {
                show_photo_upload_dialog(frm);
            });
            
            frm.add_custom_button(__('Quick Inspection'), function() {
                show_quick_inspection_dialog(frm);
            });
        }
        
        // Show photos if any
        if (frm.doc.inspection_photos) {
            show_inspection_photos(frm);
        }
    },
    
    status: function(frm) {
        if (frm.doc.status === 'Rejected') {
            frappe.msgprint({
                title: __('Quality Inspection Failed'),
                message: __('An NCR will be created automatically for this failed inspection.'),
                indicator: 'red'
            });
        }
    }
});

function show_photo_upload_dialog(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __('Upload Inspection Photos'),
        fields: [
            {
                fieldtype: 'Attach Image',
                fieldname: 'photo1',
                label: __('Photo 1')
            },
            {
                fieldtype: 'Small Text',
                fieldname: 'photo1_description',
                label: __('Photo 1 Description')
            },
            {
                fieldtype: 'Attach Image', 
                fieldname: 'photo2',
                label: __('Photo 2')
            },
            {
                fieldtype: 'Small Text',
                fieldname: 'photo2_description',
                label: __('Photo 2 Description')
            }
        ],
        primary_action: function(values) {
            // Save photos to child table
            if (values.photo1) {
                frm.add_child('inspection_photos', {
                    photo: values.photo1,
                    description: values.photo1_description || 'Inspection Photo 1'
                });
            }
            if (values.photo2) {
                frm.add_child('inspection_photos', {
                    photo: values.photo2,
                    description: values.photo2_description || 'Inspection Photo 2'
                });
            }
            frm.refresh_field('inspection_photos');
            dialog.hide();
        },
        primary_action_label: __('Upload Photos')
    });
    
    dialog.show();
}

function show_quick_inspection_dialog(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __('Quick Quality Inspection'),
        fields: [
            {
                fieldtype: 'Section Break',
                label: __('Visual Inspection')
            },
            {
                fieldtype: 'Select',
                fieldname: 'visual_check',
                label: __('Visual Check'),
                options: 'Pass\nFail',
                reqd: 1
            },
            {
                fieldtype: 'Select',
                fieldname: 'dimensional_check',
                label: __('Dimensional Check'),
                options: 'Pass\nFail',
                reqd: 1
            },
            {
                fieldtype: 'Section Break',
                label: __('Functional Tests')
            },
            {
                fieldtype: 'Select',
                fieldname: 'function_test',
                label: __('Function Test'),
                options: 'Pass\nFail',
                reqd: 1
            },
            {
                fieldtype: 'Small Text',
                fieldname: 'remarks',
                label: __('Remarks')
            }
        ],
        primary_action: function(values) {
            // Auto-populate inspection readings
            const readings = [
                {
                    specification: 'Visual Check',
                    value: values.visual_check,
                    status: values.visual_check === 'Pass' ? 'Accepted' : 'Rejected'
                },
                {
                    specification: 'Dimensional Check', 
                    value: values.dimensional_check,
                    status: values.dimensional_check === 'Pass' ? 'Accepted' : 'Rejected'
                },
                {
                    specification: 'Function Test',
                    value: values.function_test,
                    status: values.function_test === 'Pass' ? 'Accepted' : 'Rejected'
                }
            ];
            
            // Clear existing readings
            frm.clear_table('readings');
            
            // Add new readings
            readings.forEach(reading => {
                frm.add_child('readings', reading);
            });
            
            // Set overall status
            const failed_readings = readings.filter(r => r.status === 'Rejected');
            frm.set_value('status', failed_readings.length > 0 ? 'Rejected' : 'Accepted');
            frm.set_value('remarks', values.remarks);
            
            frm.refresh_fields();
            dialog.hide();
            
            frappe.msgprint({
                title: __('Quick Inspection Complete'),
                message: __('Inspection readings have been populated. Please review and save.'),
                indicator: 'green'
            });
        },
        primary_action_label: __('Complete Inspection')
    });
    
    dialog.show();
}

function show_inspection_photos(frm) {
    if (!frm.doc.inspection_photos || frm.doc.inspection_photos.length === 0) return;
    
    const photos_html = frm.doc.inspection_photos.map(photo => `
        <div class="inspection-photo" style="display: inline-block; margin: 10px;">
            <img src="${photo.photo}" style="max-width: 200px; max-height: 150px; border: 1px solid #ddd; border-radius: 4px;">
            <p style="text-align: center; font-size: 12px; margin-top: 5px;">${photo.description}</p>
        </div>
    `).join('');
    
    const photos_section = `
        <div class="inspection-photos-section">
            <h4>Inspection Photos</h4>
            <div class="photos-container">${photos_html}</div>
        </div>
    `;
    
    // Add to form
    frm.get_field('inspection_photos').$wrapper.after(photos_section);
}