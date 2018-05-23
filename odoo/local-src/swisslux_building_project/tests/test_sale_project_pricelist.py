# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestSalePricelist(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSalePricelist, cls).setUpClass()

        product = cls.env['product.product'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest product',
                'list_price': 23500,
            })
        cls.listprice = product.list_price

        cls.partner = cls.env['res.partner'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest partner'
            })

        cls.sale = cls.env['sale.order'].with_context(
            tracking_disable=True).create({
                'partner_id': cls.partner.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom': product.uom_id.id,
                    'name': '/',
                })]
            })

        cls.pricelist40 = cls.env['product.pricelist'].with_context(
            tracking_disable=True).create({
                'name': '40%',
                'item_ids': [(0, 0, {
                    'compute_price': 'percentage',
                    'percent_price': '40.0',
                })]
            })
        cls.pricelist50 = cls.env['product.pricelist'].with_context(
            tracking_disable=True).create({
                'name': '50%',
                'item_ids': [(0, 0, {
                    'compute_price': 'percentage',
                    'percent_price': '50.0',
                })]
            })

        cls.project = cls.env['building.project'].with_context(
            tracking_disable=True).create({
                'name': 'Building Project',
            })
        cls.project_pl = cls.env['building.project.pricelist'].with_context(
            tracking_disable=True).create({
                'building_project_id': cls.project.id,
                'partner_id': cls.partner.id,
            })

    def test_standard_pricelist(self):
        self.sale.button_update_unit_prices()
        self.assertAlmostEqual(self.sale.order_line.price_subtotal,
                               self.listprice)

    def test_sale_discount_pricelist(self):
        self.sale.pricelist_id = self.pricelist40
        self.sale.button_update_unit_prices()
        self.assertAlmostEqual(
            self.sale.order_line.price_subtotal,
            self.listprice * 0.6,
        )

    def test_project_without_discount(self):
        self.sale.analytic_account_id = self.project.analytic_account_id
        self.sale.button_update_unit_prices()
        self.assertAlmostEqual(
            self.sale.order_line.price_subtotal,
            self.listprice,
        )

    def test_project_discount_pricelist(self):
        self.sale.project_pricelist_id = self.pricelist50
        self.sale.button_update_unit_prices()
        self.sale.invalidate_cache()
        self.assertAlmostEqual(
            self.sale.order_line.price_subtotal,
            self.listprice * 0.5,
        )

    def test_both_discount_pricelist(self):
        self.sale.project_pricelist_id = self.pricelist50
        self.sale.pricelist_id = self.pricelist40
        self.sale.button_update_unit_prices()
        self.assertAlmostEqual(
            self.sale.order_line.price_subtotal,
            self.listprice * 0.5 * 0.6,
        )
        self.assertAlmostEqual(
            self.sale.order_line.product_id.list_price,
            23500.0
        )
