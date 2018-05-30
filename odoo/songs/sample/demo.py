# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from ..common import load_csv_no_tracking


@anthem.log
def import_customers(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/partner_customers_demo.csv', 'res.partner')


@anthem.log
def import_vendors(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/partner_vendors_demo.csv', 'res.partner')


@anthem.log
def import_both_customers_and_vendors(ctx):
    # import some partners with both profiles
    load_csv_no_tracking(
        ctx, 'data/sample/partner_customers_and_vendors_demo.csv',
        'res.partner')


@anthem.log
def import_contacts(ctx):
    # FIXME Wrong value for res.partner.property_account_receivable_id:
    # res.partner(6,)
    load_csv_no_tracking(
        ctx, 'data/sample/partner_contacts_demo.csv', 'res.partner')


@anthem.log
def import_products(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/product_demo.csv', 'product.product')


@anthem.log
def import_bauprojekt(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/bauprojekt_demo.csv', 'building.project')


@anthem.log
def main(ctx):
    """ Importing demo data """
    import_customers(ctx)
    import_vendors(ctx)
    import_both_customers_and_vendors(ctx)
    # import_contacts(ctx)
    import_products(ctx)
    import_bauprojekt(ctx)
