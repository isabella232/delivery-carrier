# Copyright 2017-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    group_id = fields.Many2one(
        'procurement.group',
        'Fixed Procurement Group',
        readonly=True,
        copy=False,
    )

    @api.model
    def _generate_finished_moves(self, production):
        move = super(MrpProduction, self)._generate_finished_moves(
            production)
        # We will get the related stock move and we will check if we have
        # a group on it
        if not move.group_id:
            move.write({'group_id': production.group_id.id})
        return move

    @api.multi
    def action_cancel(self):
        for production in self:
            moves = self.env['stock.move'].search([('group_id',
                                                    '=',
                                                    production.group_id.id),
                                                   ('move_orig_ids',
                                                    '=',
                                                    False)
                                                   ])
            moves.action_cancel()
        return super(MrpProduction, self).action_cancel()

    @api.model
    def _generate_raw_move(self, production, product, uom_id, qty):
        moves = super(MrpProduction, self)._generate_raw_move(
            production,
            product,
            uom_id,
            qty)
        for move in moves:
            if not move.group_id:
                move.write({'group_id': production.group_id.id})
            # Get previous created moves:
            previous_move_list = self.env['stock.move'].search(
                [('move_dest_id', '=', move.id)])
            for previous_move in previous_move_list:
                previous_move.write({'group_id': production.group_id.id})
        return moves
