# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    lastproduct_code = fields.Char('Last Product Code')
