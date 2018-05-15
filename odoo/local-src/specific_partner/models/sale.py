# Copyright 2015 Swisslux
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        values = {}
        if self.partner_id.is_company:
            partner = self.partner_id
        elif self.partner_id.parent_id:
            partner = self.partner_id.parent_id
        else:
            partner = self.partner_id
        if partner:
            if partner.partner_invoicing_id:
                values['partner_invoice_id'] = partner.partner_invoicing_id
            if partner.partner_shipping_id:
                values['partner_shipping_id'] = partner.partner_shipping_id
        if values:
            self.update(values)
