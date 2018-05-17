# Copyright 2017-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _propagate_procurement_group(self, group_id):
        """ Propagate the proc. group to all chain moves if propagate is True.
        Goal is to have all moves related to a same PO in a same picking all
        along the chain event if the PO has been generated from a OP.
        @return: True
        """
        res = self.write({'group_id': group_id.id, 'picking_id': False})
        self._picking_assign()
        for move in self:
            if move.move_dest_id and move.propagate:
                move.move_dest_id._propagate_procurement_group(move.group_id)
        return res
