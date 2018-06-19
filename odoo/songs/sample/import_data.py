# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update
from ..common import load_csv_no_tracking


@anthem.log
def import_regions(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/res_partner_region.csv', 'res.partner.region')


@anthem.log
def update_zip(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/res_better_zip.csv', 'res.better.zip')


@anthem.log
def import_product_categories(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/product_category.csv', 'product.category')


@anthem.log
def import_product_expenses(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/product_expenses.csv', 'product.product')


@anthem.log
def import_service_categories(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/service_artikel_kategorien.csv', 'product.category')


@anthem.log
def import_service_articles(ctx):
    # FIXME KeyError: 'product_manager'
    load_csv_no_tracking(
        ctx, 'data/sample/service_artikel.csv', 'product.product')


@anthem.log
def import_product_informations(ctx):
    load_csv_no_tracking(ctx, 'data/sample/product_class.csv', 'product.class')
    load_csv_no_tracking(
        ctx, 'data/sample/product_colorcode.csv', 'product.color.code')
    load_csv_no_tracking(
        ctx, 'data/sample/product_harmsyscode.csv', 'product.harmsys.code')
    load_csv_no_tracking(
        ctx, 'data/sample/product_manualcode.csv', 'product.manual.code')


@anthem.log
def update_reception_text_product(ctx):
    receipt_checklist = (
        "Technik (DRINGEND):\n"
        "Lieferumfang Logistik:\n\n"
        "Label aussen\n\n"
        "Label innen\n\n"
        "Anleitungen D+F\n\n"
        "Merkblatt V5.0")
    ctx.env['product.template'].search([]).write({
        'receipt_checklist': receipt_checklist,
    })


@anthem.log
def add_departement_title(ctx):
    create_or_update(
        ctx, 'res.partner.title', '__setup__.partner_title_department', {
            'name': 'Department',
        })


@anthem.log
def import_pricelists(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/product_pricelist.csv', 'product.pricelist')


@anthem.log
def import_projects(ctx):
    load_csv_no_tracking(ctx, 'data/sample/project.csv', 'project.project')


@anthem.log
def main(ctx):
    """ Importing data """
    # NOTE all scenarios tagged @slow in v9 have been omitted
    # (replaced by demo data?)
    import_regions(ctx)
    update_zip(ctx)
    import_product_categories(ctx)
    import_product_expenses(ctx)
    import_service_categories(ctx)
    # import_service_articles(ctx)
    import_product_informations(ctx)
    # import products => use demo products instead, see "demo" songs
    update_reception_text_product(ctx)
    add_departement_title(ctx)
    import_pricelists(ctx)
    import_projects(ctx)
