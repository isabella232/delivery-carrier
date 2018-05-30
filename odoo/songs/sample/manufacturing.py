# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update
from anthem.lyrics.settings import define_settings


@anthem.log
def configure_routings(ctx):
    define_settings(ctx, 'res.config.settings', {
        'group_mrp_routings': True,
    })


@anthem.log
def setup_bom_dismantling(ctx):
    ctx.env['ir.config_parameter'].create({
        'key': 'mrp.bom.dismantling.product_choice',
        'value': '1',
    })


@anthem.log
def configure_external_location(ctx):
    records = [
        {'xmlid': '__setup__.location_vendor_fluora',
         'name': 'Fluora',
         'usage': 'supplier',
         'location_id': ctx.env.ref('stock.stock_location_suppliers').id,
         'active': True,
         'return_location': False,
         'scrap_location': False,
         },
        {'xmlid': '__setup__.location_vendor_poltera',
         'name': 'Poltera',
         'usage': 'supplier',
         'location_id': ctx.env.ref('stock.stock_location_suppliers').id,
         'active': True,
         'return_location': False,
         'scrap_location': False,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'stock.location', xmlid, record)


@anthem.log
def configure_mrp_routing(ctx):
    records = [
        {'xmlid': '__setup__.mrp_routing_fluora',
         'code': 'FLUO',
         'name': 'Fluora',
         'location_id': ctx.env.ref('__setup__.location_vendor_fluora').id,
         'active': True,
         },
        {'xmlid': '__setup__.mrp_routing_poltera',
         'code': 'POLT',
         'name': 'Poltera',
         'location_id': ctx.env.ref('__setup__.location_vendor_poltera').id,
         'active': True,
         },
        {'xmlid': '__setup__.mrp_routing_intern',
         'code': 'SLX',
         'name': 'Intern',
         'location_id': ctx.env.ref('__setup__.location_vendor_poltera').id,
         'active': True,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'mrp.routing', xmlid, record)


@anthem.log
def main(ctx):
    """ Configuring manufacturing """
    configure_routings(ctx)
    setup_bom_dismantling(ctx)
    configure_external_location(ctx)
    configure_mrp_routing(ctx)
