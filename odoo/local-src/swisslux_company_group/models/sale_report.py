# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = 'sale.report'

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
            ", s.company_group_id as company_group_id," + \
            "s.income_partner_id as income_partner_id"

    def _group_by(self):
        return super()._group_by() + \
            ", s.company_group_id, s.income_partner_id"
