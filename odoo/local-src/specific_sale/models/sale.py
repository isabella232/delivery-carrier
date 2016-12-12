# -*- coding: utf-8 -*-
# © 2016 Cyril Gaudin (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class SaleOrder(models.Model):
    """ Re-active use_timesheets field on project.
    """
    _inherit = 'sale.order'

    @api.multi
    def write(self, vals):
        # Force the use of the first alias for creating tasks
        if 'client_order_ref' in vals:
            if vals['client_order_ref']:
                vals['client_order_ref'] = vals['client_order_ref'].replace(
                    ',', '/')
        res = super(SaleOrder, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        if 'client_order_ref' in vals:
            if vals['client_order_ref']:
                vals['client_order_ref'] = vals['client_order_ref'].replace(
                    ',', '/')
        res = super(SaleOrder, self).create(vals)
        return res
