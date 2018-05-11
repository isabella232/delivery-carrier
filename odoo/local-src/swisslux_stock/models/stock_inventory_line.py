# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'
    _order = "description_picking, inventory_id, location_name, " \
             "product_code, product_name, prodlot_name"

    description_picking = fields.Text(
        related='product_id.description_picking',
        store=True,
        readonly=True,
    )
