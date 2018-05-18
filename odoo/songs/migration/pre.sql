
-- Delete views which are deleted in V11 (To fix build)
-- ir.model.data will be cleaned when the original module will be updated

DELETE FROM
    ir_ui_view
WHERE
    name = 'pain.group.on.res.company.form';
