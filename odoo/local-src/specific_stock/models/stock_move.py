# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, _
from openerp.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        """ Odoo écrase les date_expected des move_dest_id lors qu'un move
        passe à done.
        Dans notre cas on veut conserver cette date pour les pickins
        venant de la Chine.
        """
        transit_loc = self.env.ref('scenario.location_transit_cn')

        expected_dates = {
            move.move_dest_id: move.move_dest_id.date_expected
            for move in self if move.move_dest_id.location_id == transit_loc
        }

        super(StockMove, self).action_done()

        for move, date_expected in expected_dates.items():
            move.date_expected = date_expected

    @api.multi
    def action_cancel(self):
        """In order to prevent to cancel a move in a supply chain, we check
        that the parent move are also cancelled"""
        if 'bypass_check_state' not in self.env.context:
            for current_stock_move in self:
                for parent_stock_move in current_stock_move.move_orig_ids:
                    if parent_stock_move.state != 'cancel':
                        raise UserError(_("You cannot cancel this move %s,"
                                          " you must first cancel "
                                          "the parent move"
                                          " in the picking %s") %
                                        (current_stock_move.name,
                                        parent_stock_move.picking_id.name))
        return super(StockMove, self).action_cancel()
