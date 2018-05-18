# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    company_group_id = fields.Many2one(
        'res.partner',
        'Company Group'
    )

    income_partner_id = fields.Many2one(
        'res.partner',
        'Income Partner'
    )

    def _select(self):
        return super()._select() + \
            ", sub.company_group_id as company_group_id," + \
            "sub.income_partner_id as income_partner_id"

    def _sub_select(self):
        return super()._sub_select() + \
            ", ai.company_group_id as company_group_id," + \
            "ai.income_partner_id as income_partner_id"

    def _group_by(self):
        return super()._group_by() + \
            ", ai.company_group_id, ai.income_partner_id"
