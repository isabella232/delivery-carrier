# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update
from anthem.lyrics.settings import define_settings


@anthem.log
def rename_basis_uom(ctx):
    create_or_update(ctx, 'product.uom', 'product.product_uom_unit', {
        'name': 'pce',
    })

    define_settings(ctx, 'res.config.settings', {
        'group_uom': True,
    })


@anthem.log
def create_taxes(ctx):
    records = [
        {'xmlid': '__setup__.tax_vrg_700180',
         'name': 'Taxe VRG 700180',
         'amount_type': 'fixed',
         'amount': 0.18,
         },
        {'xmlid': '__setup__.tax_vrg_700200',
         'name': 'Taxe VRG 700200',
         'amount_type': 'fixed',
         'amount': 0.20,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account.tax', xmlid, record)


@anthem.log
def create_accounts(ctx):
    user_type = ctx.env.ref('account.data_account_type_expenses')
    records = [
        {'xmlid': '__setup__.account_4620',
         'name': '4620',
         'code': '4620',
         'user_type_id': user_type.id,
         },
        {'xmlid': '__setup__.account_6622',
         'name': '6622',
         'code': '6622',
         'user_type_id': user_type.id,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account.account', xmlid, record)


@anthem.log
def main(ctx):
    """ Configuring products """
    rename_basis_uom(ctx)
    create_taxes(ctx)
    create_accounts(ctx)
