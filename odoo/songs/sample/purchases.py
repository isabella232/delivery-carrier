# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.settings import define_settings


@anthem.log
def set_default_tax_for_purchases(ctx):
    # TVA 8.0% sur achat B&S (TN)
    define_settings(ctx, 'res.config.settings', {
        'default_purchase_tax_id': ctx.env.ref('l10n_ch.vat_80_purchase').id,
    })


@anthem.log
def main(ctx):
    """ Configuring purchases """
    set_default_tax_for_purchases(ctx)
