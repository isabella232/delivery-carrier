# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("is_delivery", "price_unit")
    def _get_to_invoice_qty(self):
        free_delivery_lines = self.filtered(
            lambda line: line.is_delivery and line.currency_id.is_zero(line.price_unit))
        free_delivery_lines.qty_to_invoice = 0
        other_lines = self - free_delivery_lines
        super(SaleOrderLine, other_lines)._get_to_invoice_qty()
