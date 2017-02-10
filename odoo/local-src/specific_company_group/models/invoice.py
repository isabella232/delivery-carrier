# -*- coding: utf-8 -*-
# © 2015 Swisslux
# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    company_group_id = fields.Many2one(
        related='partner_id.company_group_id',
        store=True,
        readonly=True,
        model='res.partner',
        string='Company Group',
    )

    income_partner_id = fields.Many2one(
        'res.partner',
        string='Income Partner',
        domain=([('is_company', '=', True)])
    )
