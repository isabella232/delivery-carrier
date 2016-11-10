# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream, Requirement

import anthem
from anthem.lyrics.loaders import load_csv_stream


@anthem.log
def import_product_class(ctx, req):
    """ Importing product template """
    content = resource_stream(req, 'data/update/product.class.csv')
    load_csv_stream(ctx, 'product.class', content, delimiter=',')


@anthem.log
def import_product(ctx, req):
    """ Importing product template """
    content = resource_stream(req, 'data/update/product.product.csv')
    load_csv_stream(ctx, 'product.product', content, delimiter=',')


@anthem.log
def import_mrp_bom(ctx, req):
    """ Importing bom """
    content = resource_stream(req, 'data/update/mrp.bom.csv')
    load_csv_stream(ctx, 'mrp.bom', content, delimiter=',')


@anthem.log
def import_pricelist_item(ctx, req):
    """ Import  pricelist  """
    csv_content = resource_stream(
        req, 'data/update/product.pricelist.item.csv')
    load_csv_stream(ctx, 'product.pricelist.item', csv_content, delimiter=',')


@anthem.log
def import_partner_part(ctx, req, file_part):
    """ Import partner  """
    with ctx.log(u'Import Partner %s' % str(file_part)):
        csv_content = resource_stream(
            req, 'data/update/res.partner.%s.csv' % str(file_part).zfill(3))
        load_csv_stream(ctx, 'res.partner', csv_content, delimiter=',')


@anthem.log
def import_partner_contact_part(ctx, req, file_part):
    """ Import partner contact """
    with ctx.log(u'Import Partner Contact %s' % str(file_part)):
        csv_content = resource_stream(
            req,
            'data/update/res.partner_[contacts_only]).%s.csv' % str(
                file_part).zfill(3))
        load_csv_stream(ctx, 'res.partner', csv_content, delimiter=',')


@anthem.log
def import_partner_invoicing(ctx, req):
    """ Import partner invoicing  """
    csv_content = resource_stream(
        req, 'data/update/res.partner_invoiving_id.csv')
    load_csv_stream(ctx, 'res.partner', csv_content, delimiter=',')


@anthem.log
def import_product_supplier_info(ctx, req):
    """ Import  pricelist  """
    csv_content = resource_stream(
        req, 'data/update/product.supplierinfo.csv')
    load_csv_stream(ctx, 'product.supplierinfo', csv_content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading data """
    req = Requirement.parse('swisslux-odoo')
    # import_product_class(ctx, req)
    # import_product(ctx, req)
    # import_mrp_bom(ctx, req)
    # import_pricelist_item(ctx, req)
    for seq_file in xrange(1, 13):
        import_partner_part(ctx, req, seq_file)
    import_partner_invoicing(ctx, req)
    for seq_file in xrange(1, 20):
        import_partner_contact_part(ctx, req, seq_file)
    import_product_supplier_info(ctx, req)
