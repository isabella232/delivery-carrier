# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductPriceListItem(models.Model):
    _inherit = 'product.pricelist.item'
    _order = 'sequence ASC'
