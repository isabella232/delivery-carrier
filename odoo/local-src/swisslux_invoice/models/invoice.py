# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def onchange_partner_id_set_bank(self):
        """ Overwrite default partner bank if invoice bank rules are set """
        if self.partner_id and self.type in ('out_invoice', 'out_refund'):
            bank_ids = self.company_id.partner_id.bank_ids
            if not bank_ids:
                return
            rule_model = self.env['invoice.bank.rule']
            domain = [('country_id', '=', self.partner_id.country_id.id)]
            matching_rule = rule_model.search(domain, limit=1)
            if not matching_rule:
                domain = [('country_id', '=', False)]
                matching_rule = rule_model.search(domain, limit=1)
            if matching_rule:
                self.partner_bank_id = matching_rule.partner_bank_id

    @api.multi
    def invoice_validate(self):
        # Invalidate constraint that check unique reference for partner invoice
        # With some credit card company invoice reference is always the same
        return self.write({'state': 'open'})
