# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import resource_stream, Requirement

import anthem
from anthem.lyrics.loaders import load_csv_stream
from anthem.lyrics.records import create_or_update
import csv


@anthem.log
def import_product(ctx, req):
    """ Importing product template """
    content = resource_stream(req, 'data/update/product.product.csv')
    load_csv_stream(ctx, 'product.product', content, delimiter=',')

@anthem.log
def import_mrp_bom(ctx, req):
    """ Importing product template """
    content = resource_stream(req, 'data/update/mrp.bom.csv')
    load_csv_stream(ctx, 'mrp.bom', content, delimiter=',')


@anthem.log
def import_pricelist_item(ctx, req):
    """ Import Company and Individual  """
    csv_content = resource_stream(req, 'data/update/product.pricelist.item.csv')
    load_csv_stream(ctx, 'product.pricelist.item', csv_content, delimiter=',')


@anthem.log
def load_res_partner_contact(ctx, req):
    """ Import Contacts in companies  """
    csv_content = resource_stream(req, 'data/update/res.partner.contact.csv')
    load_csv_stream(ctx, 'res.partner', csv_content, delimiter=',')


@anthem.log
def main(ctx):
    """ Loading data """
    req = Requirement.parse('qoqa-odoo')
    import_product(ctx, req)
    import_mrp_bom(ctx, req)
    import_pricelist_item(ctx, req)
    # load_res_partner(ctx)
    # load_res_partner_contact(ctx)
