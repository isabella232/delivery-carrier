# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from ..common import load_csv_no_tracking


@anthem.log
def import_partner_categories(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/res_partner_category.csv', 'res.partner.category')


@anthem.log
def main(ctx):
    """ Importing partners """
    import_partner_categories(ctx)
