# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import os
from openupgradelib.openupgrade import update_module_names


@anthem.log
def fix_path_on_attachments(ctx):
    """ Fix path on attachments """
    if os.environ.get('RUNNING_ENV') == 'prod':
        # TODO: Before deployment in production, check the rancher stack name
        # Update attachment given by odoo for the database migration
        ctx.env.cr.execute("""
UPDATE
    ir_attachment
SET
    store_fname = 's3://swisslux-odoo-prod/' || store_fname
WHERE
    store_fname IS NOT NULL
AND store_fname NOT LIKE 's3://%';
        """)
    elif os.environ.get('RUNNING_ENV') == 'integration':
        # Update attachment from current production instance
        ctx.env.cr.execute("""
UPDATE
    ir_attachment
SET
    store_fname = replace(
        store_fname,
        's3://swisslux-odoo-prod/',
        's3://swisslux-odoo-integration-v11/'
    )
WHERE
    store_fname IS NOT NULL
AND store_fname LIKE 's3://%';
        """)
        # Update attachment given by odoo for the database migration
        ctx.env.cr.execute("""
UPDATE
    ir_attachment
SET
    store_fname = 's3://swisslux-odoo-integration-v11/' || store_fname
WHERE
    store_fname IS NOT NULL
AND store_fname NOT LIKE 's3://%';
        """)
    else:
        # Remove the s3 attachment
        ctx.env.cr.execute("""
DELETE FROM
    ir_attachment
WHERE
    store_fname IS NOT NULL
AND store_fname LIKE 's3://%';
        """)


@anthem.log
def rename_modules(ctx):
    """ Rename modules """
    update_module_names(
        ctx.env.cr,
        [
            ('specific_account', 'swisslux_account'),
            ('specific_building_project', 'swisslux_building_project'),
            ('specific_company_group', 'swisslux_company_group'),
            ('specific_csv_export', 'swisslux_csv_export'),
            ('specific_hr', 'swisslux_hr'),
            ('specific_invoice', 'swisslux_invoice'),
            ('specific_mrp', 'swisslux_mrp'),
            ('specific_partner', 'swisslux_partner'),
            ('specific_product', 'swisslux_product'),
            ('specific_reports', 'swisslux_reports'),
            ('specific_sale', 'swisslux_sale'),
            ('specific_stock', 'swisslux_stock'),
            ('specific_translations', 'swisslux_translations'),

            ('account_operation_rule', 'account_reconcile_rule'),
            (
                'account_operation_rule_early_payment_discount',
                'account_reconcile_rule_early_payment_discount'
            ),
        ]
    )
    update_module_names(
        ctx.env.cr,
        [
            ('account_financial_report_qweb', 'account_financial_report'),
            ('project_task_department', 'project_department'),
            ('account_permanent_lock_move', 'account_journal_lock_date'),
            ('analytic_department', 'analytic_base_department'),
        ],
        merge_modules=True,
    )


@anthem.log
def main(ctx):
    """ PRE: migration """
    fix_path_on_attachments(ctx)
    rename_modules(ctx)
