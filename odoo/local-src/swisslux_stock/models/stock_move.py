# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        """
            move_dest_id.date_expected fields are lost
            when a move is set to done
            whereas we need them for pickings coming from China.
        """
        transit_loc = self.env.ref('scenario.location_transit_cn')

        expected_dates = {
            move.move_dest_id: move.move_dest_id.date_expected
            for move in self if move.move_dest_id.location_id == transit_loc
            }

        super().action_done()

        for move, date_expected in expected_dates.items():
            move.date_expected = date_expected
