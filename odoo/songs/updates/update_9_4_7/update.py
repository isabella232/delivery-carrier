# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def cancel_picking(ctx):
    """ Cancel WH\OUT\00019 (id=177)"""
    stock_move = ctx.env['stock.move'].search(
         [('picking_id','=', 177),('state', '!=', 'done')])
    stock_move.action_cancel()


@anthem.log
def cancel_procurement_order(ctx):
    """ Cancel procurement to WH/Stock with name like 'OP%'"""
    procurement_order = ctx.env['procurement.order'].search(
         [('location_id','=', 12),('name', 'like', 'OP/'),
          ('state','!=','done'),('purchase_line_id', '=', False),
          ('name', 'not in', ('OP/00245','OP/00247'))])
    anthem.output.safe_print('Cancel and Remove %s OP' % len(procurement_order))
    procurement_order.cancel()
    procurement_order.unlink()


@anthem.log
def main(ctx):
    """ Loading data """
    cancel_picking(ctx)
    cancel_procurement_order(ctx)
