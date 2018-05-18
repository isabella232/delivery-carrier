# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestCopySalePricelistToProject(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCopySalePricelistToProject, cls).setUpClass()

        cls.product = cls.env['product.product'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest product',
                'list_price': 23500,
            })
        cls.listprice = cls.product.list_price

        cls.partner = cls.env['res.partner'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest partner'
            })

        cls.project = cls.env['building.project'].with_context(
            tracking_disable=True).create({
                'name': 'Building Project',
            })
        cls.sale = cls.env['sale.order'].with_context(
            tracking_disable=True).create({
                'partner_id': cls.partner.id,
                'order_line': [(0, 0, {
                    'product_id': cls.product.id,
                    'product_uom': cls.product.uom_id.id,
                    'name': '/',
                })],
                'analytic_account_id': cls.project.analytic_account_id.id

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

    def test_no_project_on_so(self):
        self.sale.analytic_account_id = False
        self.sale.project_pricelist_id = self.pricelist40
        self.assertEqual(len(self.project.customer_discount_ids), 0)

    def test_no_pricelist_on_so(self):
        self.sale.project_pricelist_id = False
        self.assertEqual(len(self.project.customer_discount_ids), 0)

    def test_new_pricelist_on_so(self):
        self.sale.project_pricelist_id = self.pricelist40
        self.assertEqual(len(self.project.customer_discount_ids), 1)
        self.assertEqual(self.project.customer_discount_ids.partner_id,
                         self.partner)
        self.assertEqual(self.project.customer_discount_ids.pricelist_id,
                         self.pricelist40)

    def test_new_pricelist_on_new_so(self):
        self.sale = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'name': '/',
            })],
            'analytic_account_id': self.project.analytic_account_id.id,
            'project_pricelist_id': self.pricelist40.id

        })
        self.assertEqual(len(self.project.customer_discount_ids), 1)
        self.assertEqual(self.project.customer_discount_ids.partner_id,
                         self.partner)
        self.assertEqual(self.project.customer_discount_ids.pricelist_id,
                         self.pricelist40)

    def test_existing_pricelist(self):
        """ Setting a pricelist for a customer listed in project discount
        doesn't change the pricelist
        """
        self.project_pl = self.env['building.project.pricelist'].create({
            'building_project_id': self.project.id,
            'partner_id': self.partner.id,
            'pricelist_id': self.pricelist40.id,
        })
        self.sale.pricelist_id = self.pricelist50
        self.assertEqual(len(self.project.customer_discount_ids), 1)
        self.assertEqual(self.project.customer_discount_ids.partner_id,
                         self.partner)
        self.assertEqual(self.project.customer_discount_ids.pricelist_id,
                         self.pricelist40)
