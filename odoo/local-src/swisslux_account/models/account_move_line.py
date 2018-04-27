# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        return_val = super()._prepare_payment_line_vals(
            payment_order)
        if not return_val['partner_bank_id']:
            partner_bank_obj = self.env['res.partner.bank']
            partner_bank_id = partner_bank_obj.search([
                ('partner_id', '=', return_val['partner_id'])], limit=1)
            if partner_bank_id:
                return_val['partner_bank_id'] = partner_bank_id.id
        return return_val
