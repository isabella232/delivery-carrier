# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


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
        res = super().write(vals)
        return res

    @api.model
    def create(self, vals):
        if 'client_order_ref' in vals:
            if vals['client_order_ref']:
                vals['client_order_ref'] = vals['client_order_ref'].replace(
                    ',', '/')
        res = super().create(vals)
        return res
