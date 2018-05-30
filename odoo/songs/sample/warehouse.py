# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update
from anthem.lyrics.settings import define_settings


@anthem.log
def update_settings(ctx):
    # FIXME: no longer existing or renamed parameters:
    # set "Inventory Valuation" to "Periodic inventory valuation (recommended)"
    # set "Dropshipping" to "Allow suppliers to deliver directly to your
    # customers"
    define_settings(ctx, 'res.config.settings', {
        'module_stock_barcode': True,
        'group_stock_production_lot': True,
        'group_stock_adv_location': True,
        'group_stock_multi_locations': True,
    })


@anthem.log
def configure_main_warehouse(ctx):
    create_or_update(ctx, 'stock.warehouse', 'stock.warehouse0', {
        'name': 'Swisslux AG',
        'reception_steps': 'three_steps',
        'delivery_steps': 'ship_only',
    })


@anthem.log
def configure_china_transit_location(ctx):
    create_or_update(ctx, 'stock.location', '__setup__.location_transit_cn', {
        'name': 'Swisslux AG: Departure from China',
        'usage': 'transit',
        'location_id': ctx.env.ref('stock.stock_location_locations').id,
        'active': True,
        'return_location': False,
        'scrap_location': False,
    })


@anthem.log
def configure_china_picking(ctx):
    sequence = ctx.env['ir.sequence'].search([
        ('name', '=', 'Swisslux AG Sequence in'),
    ], limit=1)
    create_or_update(
        ctx, 'stock.picking.type', '__setup__.picking_type_receive_cn', {
            'name': 'Receive from China',
            'default_location_dest_id': ctx.env.ref(
                '__setup__.location_transit_cn').id,
            'code': 'incoming',
            'sequence_id': sequence.id,
            'warehouse_id': ctx.env.ref('stock.warehouse0').id,
            'return_picking_type_id': ctx.env.ref('stock.picking_type_out').id,
        })


@anthem.log
def add_global_push_rule(ctx):
    # FIXME route_id is now required in stock.location.path
    # What is the appropriate route id here? __setup__.location_route?
    route_id = 2
    create_or_update(
        ctx, 'stock.location.path', '__setup__.location_path_transit_to_slx', {
            'name': 'Receive from China',
            'active': True,
            'location_from_id': ctx.env.ref(
                '__setup__.location_transit_cn').id,
            'location_dest_id': ctx.env.ref('stock.stock_location_company').id,
            'auto': 'manual',
            'picking_type_id': ctx.env.ref('stock.picking_type_in').id,
            'delay': 0,
            'route_id': route_id,
        })


@anthem.log
def set_procurement_rule(ctx):
    ctx.env['procurement.rule'].search([
        ('name', '=', 'Swisslux AG:  Buy'),
    ]).write({
        'propagate': True,
        'group_propagation_option': 'propagate',
    })


@anthem.log
def set_default_company_reception_text(ctx):
    text = ("_____ Anleitung Deutsch\n"
            "_____ Anleitung Franz.\n"
            "_____ Anleitung Ital.\n"
            "_____ Verpackung\n"
            "_____ Lieferumfang\n"
            "_____ Funktionstest\n\n"
            "Charge: __________________________\n\n"
            "Technik:\n"
            "Produktenews: JA / NEIN\n"
            "Visum: ____________________________")
    ctx.env['res.company'].search([]).write({
        'receipt_checklist': text,
    })


@anthem.log
def configure_occasion(ctx):
    location = ctx.env['stock.location'].search([
        ('name', '=', 'WH'),
    ], limit=1)
    create_or_update(ctx, 'stock.location', '__setup__.location_occasion', {
        'name': 'Vorrat',
        'usage': 'internal',
        'location_id': location.id,
        'active': True,
        'return_location': True,
        'scrap_location': False,
    })

    sequence = ctx.env['ir.sequence'].search([
        ('name', '=', 'Swisslux AG Sequence in'),
    ], limit=1)
    create_or_update(
        ctx, 'stock.picking.type', '__setup__.picking_type_occasion', {
            'name': 'Vorrat Sendung',
            'default_location_dest_id': ctx.env.ref(
                'stock.stock_location_customers').id,
            'default_location_src_id': ctx.env.ref(
                '__setup__.location_occasion').id,
            'code': 'outgoing',
            'use_existing_lots': True,
            'active': True,
            'sequence_id': sequence.id,
            'warehouse_id': ctx.env.ref('stock.warehouse0').id,
            'return_picking_type_id': ctx.env.ref('stock.picking_type_out').id,
        })

    create_or_update(ctx, 'stock.location.route', '__setup__.location_route', {
        'name': 'Swisslux AG: Vorrat Sendung',
        'product_selectable': True,
        'sale_selectable': True,
        'product_categ_selectable': True,
        'warehouse_selectable': True,
        'active': True,
        'sequence': 10,
        'warehouse_ids': [(6, False, [ctx.env.ref('stock.warehouse0').id])],
    })

    create_or_update(
        ctx, 'procurement.rule', '__setup__.procurement_rule_occasion', {
            'action': 'move',
            'active': True,
            'procure_method': 'make_to_stock',
            'name': 'WH: Vorrat -> Customers',
            'delay': 0,
            'picking_type_id': ctx.env.ref(
                '__setup__.picking_type_occasion').id,
            'location_id': ctx.env.ref('stock.stock_location_customers').id,
            'route_sequence': 10,
            'sequence': 20,
            'warehouse_id': ctx.env.ref('stock.warehouse0').id,
            'route_id': ctx.env.ref('__setup__.location_route').id,
            'location_src_id': ctx.env.ref('__setup__.location_occasion').id,
            'propagate': True,
        })

    create_or_update(ctx, 'stock.location.route', '__setup__.location_route', {
        'pull_ids': [
            (6, False, [ctx.env.ref('__setup__.procurement_rule_occasion').id])
        ],
    })


@anthem.log
def configure_return(ctx):
    location = ctx.env['stock.location'].search([
        ('name', '=', 'WH'),
    ], limit=1)
    records = [
        {'xmlid': '__setup__.location_retour_in',
         'name': 'Retouren (Eingang)',
         'usage': 'internal',
         'location_id': location.id,
         'active': True,
         'return_location': True,
         'scrap_location': False,
         },
        {'xmlid': '__setup__.location_retour_qc',
         'name': 'Retouren (Qualität)',
         'usage': 'internal',
         'location_id': location.id,
         'active': True,
         'return_location': True,
         'scrap_location': False,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'stock.location', xmlid, record)

    sequence = ctx.env['ir.sequence'].search([
        ('name', '=', 'Swisslux AG Sequence in'),
    ], limit=1)
    records = [
        {'xmlid': '__setup__.picking_type_retour',
         'name': 'Retouren (receipt)',
         'default_location_dest_id': ctx.env.ref(
             '__setup__.location_retour_in').id,
         'default_location_src_id': ctx.env.ref(
             'stock.stock_location_customers').id,
         'code': 'incoming',
         'use_existing_lots': True,
         'active': True,
         'sequence_id': sequence.id,
         'warehouse_id': ctx.env.ref('stock.warehouse0').id,
         },
        {'xmlid': '__setup__.picking_type_retour_int',
         'name': 'Retouren (internal transfer)',
         'default_location_dest_id': ctx.env.ref(
             '__setup__.location_retour_qc').id,
         'default_location_src_id': ctx.env.ref(
             '__setup__.location_retour_qc').id,
         'code': 'internal',
         'use_existing_lots': True,
         'active': True,
         'sequence_id': sequence.id,
         'warehouse_id': ctx.env.ref('stock.warehouse0').id,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'stock.picking.type', xmlid, record)

    create_or_update(
        ctx, 'stock.location.route', '__setup__.location_route_retour', {
            'name': 'Swisslux AG: Retouren für Kontrolle',
            'product_selectable': True,
            'sale_selectable': True,
            'product_categ_selectable': True,
            'warehouse_selectable': True,
            'active': True,
            'sequence': 10,
            'warehouse_ids': [
                (6, False, [ctx.env.ref('stock.warehouse0').id])
            ],
        })

    create_or_update(
        ctx, 'stock.location.path', '__setup__.location_path_retour', {
            'active': True,
            'auto': 'manual',
            'location_from_id': ctx.env.ref('__setup__.location_retour_in').id,
            'location_dest_id': ctx.env.ref('__setup__.location_retour_qc').id,
            'name': 'WH: Retour Input -> Retour Quality Control',
            'picking_type_id': ctx.env.ref(
                '__setup__.picking_type_retour_int').id,
            'propagate': True,
            'route_id': ctx.env.ref('__setup__.location_route_retour').id,
        })

    create_or_update(
        ctx, 'stock.location.route', '__setup__.location_route_retour', {
            'push_ids': [
                (6, False, [ctx.env.ref('__setup__.location_path_retour').id])
            ],
        })


@anthem.log
def main(ctx):
    """ Configuring warehouses """
    update_settings(ctx)
    configure_main_warehouse(ctx)
    configure_china_transit_location(ctx)
    configure_china_picking(ctx)
    add_global_push_rule(ctx)
    set_procurement_rule(ctx)
    set_default_company_reception_text(ctx)
    configure_occasion(ctx)
    configure_return(ctx)
