# -*- coding: utf-8 -*-
# © 2015 Swisslux
# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    company_group_id = fields.Many2one(
        related='partner_id.company_group_id',
        model='res.partner',
        store=True,
        string='Company Group',
    )

    # The partner that will be invoiced
    income_partner_id = fields.Many2one(
        related='partner_invoice_id.commercial_partner_id',
        model='res.partner',
        store=True,
        readonly=True,
        string='Income Commercial Partner',
    )

    # The partner where the order will be sent
    commercial_partner_id = fields.Many2one(
        related='partner_id.commercial_partner_id',
        model='res.partner',
        store=True,
        readonly=True,
        string='Commercial Entity',
    )

    @api.multi
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals['income_partner_id'] = self.partner_id.id
        return vals


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice_return = super(SaleAdvancePaymentInv, self)._create_invoice(
            order, so_line, amount)
        invoice_return.income_partner_id = order.partner_id.id
        return invoice_return
