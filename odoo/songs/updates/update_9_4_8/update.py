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
    # Create procurement rule first
    values = {
        'name': "Swisslux AG: Buy from China",
        'sequence': 20,
        'action': "buy",
        'active': True,
        'group_propagation_option': "propagate",
        'location_id': 18,
        'picking_type_id': 7,
        'delay': 0,
        'warehouse_id': 1,
        'propagate': True,
        'procure_method': "make_to_stock",
        'route_sequence': 1,
    }
    create_or_update(ctx, 'procurement.rule',
                     '__upgrade948__.procurement_rule_china', values)

    values = {
        'name': "WH:  Departure from China-> Input",
        'sequence': 20,
        'action': "move",
        'active': True,
        'group_propagation_option': "propagate",
        'location_id': 13,
        'location_src_id': 18,
        'picking_type_id': 1,
        'delay': 0,
        'warehouse_id': 1,
        'propagate': True,
        'procure_method': "make_to_order",
        'route_sequence': 1,
    }
    create_or_update(ctx, 'procurement.rule',
                     '__upgrade948__.procurement_rule_input', values)

    values = {
        'name': "Buy from China",
        'sequence': 1,
        'warehouse_selectable': False,
        'product_selectable': True,
        'product_categ_selectable': False,
        'sale_selectable': False,
        'pull_ids': [
            (6, 0, [ctx.env.ref(
                '__upgrade948__.procurement_rule_china').id,
                ctx.env.ref(
                '__upgrade948__.procurement_rule_input').id])]
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
