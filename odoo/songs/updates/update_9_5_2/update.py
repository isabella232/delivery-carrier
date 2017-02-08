# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem

@anthem.log
def set_report_base_url(ctx):
    """ Configuring web.base.url """
    url = 'http://localhost:8069'
    ctx.env['ir.config_parameter'].set_param('report.url', url)

def get_child_move(ctx,stock_move, chain_move=[]):
    if stock_move.state not in ['done', 'cancel']:
        chain_move.append(stock_move.id)
    if stock_move.move_dest_id:
        get_child_move(ctx, stock_move.move_dest_id, chain_move)
    return chain_move

@anthem.log
def recreate_routing(ctx):
    """ Recreate routing from PO see ticket #3731 """
    """ Get all move that start from input and departure from china"""

    stock_move_list = ctx.env['stock.move'].search([
        ('location_id', 'in', [13, 18]),
        ('id', 'not in', [715, 752, 6439, 731, 737, 749, 728])])
    cpt = 1
    for stock_move in stock_move_list:
        #We will search the the stock_move_releated
        chaine_move_id = get_child_move(ctx, stock_move, [])
        anthem.output.safe_print(
            'Cancel move and and child %s-%s %s' % (cpt, len(stock_move_list), chaine_move_id))
        to_cancel_moves = ctx.env['stock.move'].search([
            ('id', 'in', chaine_move_id)])
        for cancel_move in to_cancel_moves:
            cancel_move.state = 'cancel'
        cpt+=1
    # Get all stock picking from location vendor that is not done or cancel
    picking_list = ctx.env['stock.picking'].search([
        ('location_id', '=', [8]),
        ('state', 'not in', ['done', 'cancel'])])
    cpt = 1
    for stock_picking in picking_list:
        anthem.output.safe_print(
            'Cancel picking %s-%s-%s ' % (stock_picking.id,cpt, len(picking_list)))
        stock_picking.action_cancel()
        new_picking = stock_picking.copy()
        new_picking.action_confirm()
        cpt += 1



@anthem.log
def main(ctx):
    """ Loading data """
    set_report_base_url(ctx)
    recreate_routing(ctx)
