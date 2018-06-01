# Copyright 2015 Swisslux
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    company_group_id = fields.Many2one(
        comodel_name='res.partner',
        string='Company Group',
    )

    company_group_readonly_id = fields.Many2one(
        related='company_group_id',
        readonly=True,
    )

    income_partner_id = fields.Many2one(
        'res.partner',
        string='Income Partner',
        domain=([('is_company', '=', True)])
    )

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.company_group_id = self.partner_id.company_group_id.id
        else:
            self.company_group_id = None
