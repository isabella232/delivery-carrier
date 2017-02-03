# -*- coding: utf-8 -*-

from openerp import models, fields


class sale_report(models.Model):
    _inherit = 'sale.report'

    company_group_id = fields.Many2one(
        'res.partner',
        'Company Group'
    )

    def _select(self):
        return super(sale_report, self).\
                   _select() + ", s.company_group_id as company_group_id"

    def _group_by(self):
        return super(sale_report, self). \
                   _group_by() + ", s.company_group_id"
