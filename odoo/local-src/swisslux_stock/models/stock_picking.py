# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one(states={})
