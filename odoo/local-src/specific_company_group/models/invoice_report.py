# -*- coding: utf-8 -*-

from openerp import models, fields


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
        return super(AccountInvoiceReport, self).\
            _select() + ", sub.company_group_id as company_group_id," + \
            "sub.income_partner_id as income_partner_id"

    def _sub_select(self):
        return super(AccountInvoiceReport, self). \
            _sub_select() + ", ai.company_group_id as company_group_id," + \
            "ai.income_partner_id as income_partner_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self). \
                   _group_by() + ", ai.company_group_id, ai.income_partner_id"
