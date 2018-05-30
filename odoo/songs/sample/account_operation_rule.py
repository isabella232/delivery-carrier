# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def create_account_operation_rule(ctx):
    values = {
        'name': 'Skonti',
        'code': '4090',
        'user_type_id': ctx.env.ref(
            'account.data_account_type_expenses').id,
        'internal_type': 'other',
    }
    create_or_update(ctx, 'account.account',
                     '__setup__.account_4090', values)

    values = {
        'name': 'Skonto',
        'label': 'Skonto',
        'company_id': ctx.env.ref('base.main_company').id,
        'account_id': ctx.env.ref('__setup__.account_4090').id,
        'journal_id': ctx.env.ref('__setup__.journal_ZKB1').id,
        'amount_type': 'percentage',
        'amount': 100,
        # TVA due à 8.0% (Incl. TN):
        'tax_id': ctx.env.ref('l10n_ch.vat_80_incl').id,
    }
    create_or_update(ctx, 'account.reconcile.model',
                     '__setup__.account_operation_template_skonto', values)

    values = {
        'name': 'Skonto',
        'rule_type': 'early_payment_discount',
        'reconcile_model_ids': [(6, False, [ctx.env.ref(
            '__setup__.account_operation_template_skonto').id])],
    }
    create_or_update(ctx, 'account.reconcile.rule',
                     '__setup__.account_operation_rule_skonto', values)


@anthem.log
def main(ctx):
    """ Configuring operation rules """
    create_account_operation_rule(ctx)
