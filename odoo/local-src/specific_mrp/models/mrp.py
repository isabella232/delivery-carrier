# -*- coding: utf-8 -*-
# © 2017 Vincent Renaville (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    group_id = fields.Many2one(
        'procurement.group',
        'Fixed Procurement Group',
        readonly=True,
    )

    @api.multi
    def action_confirm(self):
        for production in self:
            production.group_id = self.env['procurement.group'].create(
                {'name': production.name})
        return super(MrpProduction, self).action_confirm()

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({'group_id': False})
        return super(MrpProduction, self).copy(default)

    @api.model
    def _make_production_produce_line(self, production):
        created_ids = super(MrpProduction, self)._make_production_produce_line(
            production)
        # We will get the related stock move and we will check if we have
        # a group on it
        for move in self.env['stock.move'].browse(created_ids):
            if not move.group_id:
                move.write({'group_id': production.group_id.id})
        return created_ids

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
    def _make_consume_line_from_data(self, production, product, uom_id, qty):
        move_id = super(MrpProduction, self)._make_consume_line_from_data(
            production,
            product,
            uom_id,
            qty)
        move = self.env['stock.move'].browse(move_id)
        if not move.group_id:
            move.write({'group_id': production.group_id.id})
        # Get previous created moves:
        previous_move_list = self.env['stock.move'].search(
            [('move_dest_id', '=', move_id)])
        for previous_move in previous_move_list:
            previous_move.write({'group_id': production.group_id.id})
        return move_id
