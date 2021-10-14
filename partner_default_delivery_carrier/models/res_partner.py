# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_partner_default_delivery_carrier_id(self):
        return self.env.company.partner_default_delivery_carrier_id

    property_delivery_carrier_id = fields.Many2one(
        default=_get_partner_default_delivery_carrier_id,
    )
