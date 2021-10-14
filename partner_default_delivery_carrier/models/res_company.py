# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_default_delivery_carrier_id = fields.Many2one(
        "delivery.carrier",
        string="Partner Default Delivery Method",
    )
