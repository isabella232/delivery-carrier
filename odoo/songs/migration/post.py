# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.modules import uninstall


@anthem.log
def uninstall_modules(ctx):
    """ Uninstall modules """
    uninstall(
        ctx,
        [
            'mrp_bom_dismantling',
            'l10n_ch_payment_slip',
            'delivery_carrier_label_s3',
            'specific_timesheet',
            'specific_timesheet_activities',
        ]
    )


@anthem.log
def clean_modules_list(ctx):
    """ Clean modules list """
    modules = ctx.env['ir.module.module'].search([
        (
            'name',
            'in',
            (
                'mrp_bom_dismantling',
                'l10n_ch_payment_slip',
                'delivery_carrier_label_s3',
                'specific_timesheet',
                'specific_timesheet_activities',
            )
        ),
    ])
    modules.write({
        'state': 'uninstallable'
    })
    modules.unlink()


@anthem.log
def clean_duplicated_menu(ctx):
    """ Clean duplicated menu """
    executive_summary_menu_to_delete = ctx.env.ref(
        '__export__.ir_ui_menu_218',
        raise_if_not_found=False,
    )
    if executive_summary_menu_to_delete:
        executive_summary_menu_to_keep = ctx.env.ref(
            'account_reports.account_financial_html_report_menu_4',
        )
        action_to_delete = executive_summary_menu_to_delete.action
        action_to_keep = executive_summary_menu_to_keep.action
        executive_summary_menu_to_keep.write({
            'action':
                '%s,%s' % (action_to_keep._name, action_to_keep.id),
            'groups_id':
                [(6, False, executive_summary_menu_to_delete.groups_id.ids)]
        })
        action_to_delete.unlink()
        executive_summary_menu_to_delete.unlink()


@anthem.log
def migrate_account_reconcile_rule_values(ctx):
    """ Migrate account reconcile rule values """
    if not ctx.env['account.reconcile.rule'].search([]):
        # if account reconcile rule not found, we need
        # to migrate the previous values in account_operation_rule table
        ctx.env.cr.execute("""
INSERT INTO
    account_reconcile_rule
SELECT
    id,
    name,
    rule_type,
    amount_min,
    amount_max,
    sequence,
    create_uid,
    create_date,
    write_uid,
    write_date
FROM
    account_operation_rule;
    """)
    ctx.env.cr.execute("""
INSERT INTO
    account_reconcile_model_account_reconcile_rule_rel
SELECT
    account_operation_rule_id AS account_reconcile_rule_id,
    account_operation_template_id AS account_reconcile_model_id
FROM
    account_operation_rule_account_operation_template_rel;
        """)


@anthem.log
def set_project_task_type_inactive(ctx):
    """Set project.task.type from project_task_default_stage to inactive"""
    project_task_types = ctx.env['project.task.type']
    records = [
        'project_tt_analysis',
        'project_tt_specification',
        'project_tt_design',
        'project_tt_development'
        'project_tt_testing',
        'project_tt_merge',
        'project_tt_deployment',
        'project_tt_cancel'
    ]
    for rec in records:
        project_task_types |= ctx.env.ref(
            'project_task_default_stage.%s' % rec, raise_if_not_found=False)
    project_task_types.write({'active': False})


@anthem.log
def main(ctx):
    """ POST: migration """
    uninstall_modules(ctx)
    clean_modules_list(ctx)
    clean_duplicated_menu(ctx)
    migrate_account_reconcile_rule_values(ctx)
    set_project_task_type_inactive(ctx)
