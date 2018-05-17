# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from openupgradelib.openupgrade import update_module_names


@anthem.log
def rename_modules(ctx):
    """ Rename modules """
    update_module_names(
        ctx.env.cr,
        [
            ('specific_account', 'swisslux_account'),
            ('specific_hr', 'swisslux_hr'),
            ('specific_invoice', 'swisslux_invoice'),
            ('specific_mrp', 'swisslux_mrp'),
            ('specific_partner', 'swisslux_partner'),
            ('specific_product', 'swisslux_product'),
            ('specific_purchase', 'swisslux_purchase'),
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
    rename_modules(ctx)
