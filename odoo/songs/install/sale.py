# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.settings import define_settings


@anthem.log
def setup_proforma_invoice(ctx):
    define_settings(
        ctx,
        'res.config.settings',
        {
            'group_proforma_sales': True,
        })


@anthem.log
def main(ctx):
    setup_proforma_invoice(ctx)
