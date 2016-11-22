# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def reload_translation(ctx, module):
    """ update translation """
    ctx.env['ir.module.module'].with_context(overwrite=True).search(
        [('name', '=', module)]).update_translations()


@anthem.log
def create_new_route(ctx):
    """ Create new route Buy from China """
    values = {
        'name': "Buy from China",
        'sequence': "1",
        'warehouse_selectable': False,
        'product_selectable': True,
        'product_categ_selectable': False,
        'sale_selectable': False,
    }
    create_or_update(ctx, 'stock.location.route',
                     '__upgrade948__.stock_location_route_china', values)
    # Get the id of the route buy to remove it from selection
    buy_route = ctx.env['stock.location.route'].search([('name', '=', 'Buy')])
    # We will set on product the china route by default
    china_country = ctx.env['res.country'].search([('name', '=', 'China')])
    partner_china = ctx.env['res.partner'].search(
        [('country_id', '=', china_country.id)])
    china_partner_ids = [x.id for x in partner_china]
    product_supplierinfochina = ctx.env['product.supplierinfo'].search(
        [('name', 'in', china_partner_ids)])
    for productsupplier in product_supplierinfochina:
        productsupplier.product_tmpl_id.write({'route_ids': [(
            4, ctx.env.ref('__upgrade948__.stock_location_route_china').id)]})
        # Remove the Buy Route
        productsupplier.product_tmpl_id.write({'route_ids': [(
            3, buy_route.id)]})


@anthem.log
def main(ctx):
    """ Loading data """
    reload_translation(ctx, 'specific_reports')
    create_new_route(ctx)
