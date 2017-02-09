# -*- coding: utf-8 -*-

from openerp import models, fields


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
        return super(SaleReport, self).\
            _select() + ", s.company_group_id as company_group_id," + \
            "s.income_partner_id as income_partner_id"

    def _group_by(self):
        return super(SaleReport, self). \
                   _group_by() + ", s.company_group_id, s.income_partner_id"
