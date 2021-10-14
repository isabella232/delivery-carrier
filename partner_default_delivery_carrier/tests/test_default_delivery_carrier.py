# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestPackageFee(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Company 0: no default delivery carrier
        cls.company0 = cls.env["res.company"].create(
            {
                "name": "S.H.I.E.L.D.",
                "partner_default_delivery_carrier_id": False,
            }
        )

        # Company 1: default delivery carrier 1
        cls.carrier1 = cls.env["delivery.carrier"].create(
            {
                "name": "Delivery1",
                "fixed_price": 1.0,
                "product_id": cls.env["product.product"].create(
                    {"name": "Shipping1", "type": "service"}
                ).id,
            }
        )
        cls.company1 = cls.env["res.company"].create(
            {
                "name": "Avengers",
                "partner_default_delivery_carrier_id": cls.carrier1.id,
            }
        )

        # Company 2: default delivery carrier 2
        cls.carrier2 = cls.env["delivery.carrier"].create(
            {
                "name": "Delivery2",
                "fixed_price": 2.0,
                "product_id": cls.env["product.product"].create(
                    {"name": "Shipping2", "type": "service"}
                ).id,
            }
        )
        cls.company2 = cls.env["res.company"].create(
            {
                "name": "Sinister Six",
                "partner_default_delivery_carrier_id": cls.carrier2.id,
            }
        )

        # Allow user to use the new companies
        cls.env.user.company_ids |= cls.company0 + cls.company1 + cls.company2

    def _create_partner(self, company):
        vals = {"name": "MockupPartner"}
        return self.env["res.partner"].with_company(company).create(vals)

    def test_00_partner_create(self):
        for company in self.env.companies:
            self.assertEqual(
                self._create_partner(company).property_delivery_carrier_id.id,
                company.partner_default_delivery_carrier_id.id
            )
