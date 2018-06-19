# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.settings import define_settings


@anthem.log
def configure_sales(ctx):
    define_settings(ctx, 'res.config.settings', {
        'default_invoice_policy': 'delivery',
        'group_discount_per_so_line': True,
        'sale_pricelist_setting': 'formula',
        # TVA due à 8.0% (Incl. TN):
        'default_sale_tax_id': ctx.env.ref('l10n_ch.vat_80_incl').id,
        'group_sale_delivery_address': True,
        'group_sale_pricelist': True,
        'group_pricelist_item': True,
        'group_route_so_lines': True,
    })


@anthem.log
def main(ctx):
    """ Configuring sales """
    configure_sales(ctx)
