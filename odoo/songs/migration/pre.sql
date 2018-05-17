
--   Reset 'state' of ir_module_module
--
--   When we receive the database from the migration service, addons are
--   'to upgrade', set them to uninstalled.
UPDATE
    ir_module_module
SET
    state = 'uninstalled'
WHERE
    state IN ('to install', 'to upgrade')
AND
    name NOT IN (
        'mrp_bom_dismantling',
        'l10n_ch_payment_slip',
        'delivery_carrier_label_s3',
        'specific_timesheet',
        'specific_timesheet_activities'
    );


-- Delete views which are deleted in V11 (To fix build)
-- ir.model.data will be cleaned when the original module will be updated

DELETE FROM
    ir_ui_view
WHERE
    name = 'pain.group.on.res.company.form';

DELETE FROM
    ir_ui_view
WHERE
    id IN (
        SELECT
            res_id
        FROM
            ir_model_data
        WHERE
            module IN (
                'project_task_department',
                'specific_timesheet',
                'specific_timesheet_activities'
            )
        AND
            model = 'ir.ui.view'
    );
