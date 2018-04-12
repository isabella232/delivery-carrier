# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductClass(models.Model):
    _name = 'product.class'
    name = fields.Char(required=True)
