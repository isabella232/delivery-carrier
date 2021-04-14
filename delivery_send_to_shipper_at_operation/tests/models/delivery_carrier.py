# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    def send_shipping(self, pickings):
        # Hardcode returned values as we have no carrier provider during test
        return [{"exact_price": 10.0, "tracking_number": "TEST"}]
