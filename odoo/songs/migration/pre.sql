
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
                'l10n_ch_payment_slip',
                'project_task_department',
                'specific_timesheet',
                'specific_timesheet_activities'
            )
        AND
            model = 'ir.ui.view'
    );


-- Update mrp.production to use procurement_group_id (defined in odoo/mrp)
-- instead of group_id which was defined in v9 in specific_mrp
UPDATE
    mrp_production
SET
    procurement_group_id = group_id;

-- Remove unneeded group_id column on mrp_production
ALTER TABLE
    mrp_production
DROP COLUMN
    group_id;
