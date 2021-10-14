# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    partner_default_delivery_carrier_id = fields.Many2one(
        "delivery.carrier",
        readonly=False,
        related="company_id.partner_default_delivery_carrier_id",
    )
