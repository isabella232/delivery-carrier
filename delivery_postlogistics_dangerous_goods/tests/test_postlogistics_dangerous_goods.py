# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from os.path import dirname, join

from odoo import exceptions
from odoo.tests.common import SavepointCase

from vcr import VCR

from ..postlogistics.web_service import PostlogisticsWebServiceDangerousGoods

recorder = VCR(
    record_mode="once",
    cassette_library_dir=join(dirname(__file__), "fixtures/cassettes"),
    path_transformer=VCR.ensure_suffix(".yaml"),
    filter_headers=["Authorization"],
    # ignore scheme, host, port
    match_on=("method", "path", "query"),
    # allow to read and edit content in cassettes
    decode_compressed_response=True,
)

ENDPOINT_URL = "https://wedecint.post.ch/"
CLIENT_ID = "XXX"
CLIENT_SECRET = "XXX"
LICENSE = "XXX"


class TestPostlogisticsDangerousGoods(SavepointCase):
    at_install = False
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        license_id = cls.env["postlogistics.license"].create(
            {"name": "TEST", "number": LICENSE}
        )
        Product = cls.env["product.product"]
        partner_id = cls.env.ref("delivery_postlogistics.partner_postlogistics").id
        OptionTmpl = cls.env["postlogistics.delivery.carrier.template.option"]
        label_layout = OptionTmpl.create({"code": "A6", "partner_id": partner_id})
        output_format = OptionTmpl.create({"code": "PDF", "partner_id": partner_id})
        image_resolution = OptionTmpl.create({"code": "600", "partner_id": partner_id})

        cls.carrier = cls.env["delivery.carrier"].create(
            {
                "name": "Postlogistics",
                "delivery_type": "postlogistics",
                "product_id": Product.create({"name": "Shipping"}).id,
                "postlogistics_endpoint_url": ENDPOINT_URL,
                "postlogistics_license_id": license_id.id,
                "postlogistics_client_id": CLIENT_ID,
                "postlogistics_client_secret": CLIENT_SECRET,
                "postlogistics_label_layout": label_layout.id,
                "postlogistics_output_format": output_format.id,
                "postlogistics_resolution": image_resolution.id,
            }
        )

        # Create Product packaging
        product_packaging_model = cls.env["product.packaging"]
        cls.postlogistics_packaging = product_packaging_model.create(
            {
                "name": "PRI-PACKAGING",
                "package_carrier_type": "postlogistics",
                "shipper_package_code": "PRI",
            }
        )

        # Create UNNumbers
        un_reference_model = cls.env["un.reference"]
        unnumber_valid = un_reference_model.create(
            {"name": "1234", "description": "Valid UNNumber"}
        )
        unnumber_non_valid = un_reference_model.create(
            {"name": "1234,", "description": "Non-valid UNNumber"}
        )

        limited_amount_lq = cls.env.ref("l10n_eu_product_adr.limited_amount_1")

        # Create products
        cls.product_lq = cls.env["product.product"].create(
            {
                "name": "Product LQ",
                "un_ref": unnumber_valid.id,
                "limited_amount_id": limited_amount_lq.id,
                "is_dangerous": True,
                "is_dangerous_good": True,
            }
        )
        cls.product_lq_wrong_number = cls.env["product.product"].create(
            {
                "name": "Product LQ wrong UNNumber",
                "un_ref": unnumber_non_valid.id,
                "limited_amount_id": limited_amount_lq.id,
                "is_dangerous": True,
                "is_dangerous_good": True,
            }
        )
        cls.product_no_lq = cls.env["product.product"].create({"name": "Product no LQ"})

        cls.company = cls.env.user.company_id
        cls.company.write(
            {
                "street": "Rue de Lausanne 1",
                "zip": "1030",
                "city": "Bussigny",
                "name": "My Company",
            }
        )
        cls.company.partner_id.country_id = cls.env.ref("base.ch")
        cls.env.user.lang = "en_US"

    def create_picking(self, products_matrix):
        stock_location = self.env.ref("stock.stock_location_stock")
        customer_location = self.env.ref("stock.stock_location_customers")
        recipient = self.env["res.partner"].create(
            {
                "name": "Camptocamp SA",
                "street": "EPFL Innovation Park, Bât A",
                "zip": "1015",
                "city": "Lausanne",
            }
        )
        picking = self.env["stock.picking"].create(
            {
                "partner_id": recipient.id,
                "carrier_id": self.carrier.id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": stock_location.id,
                "location_dest_id": customer_location.id,
            }
        )
        stock_move_model = self.env["stock.move"]
        for product, qty in products_matrix:
            stock_move_model.create(
                {
                    "name": product.name,
                    "product_id": product.id,
                    "product_uom_qty": qty,
                    "product_uom": product.uom_id.id,
                    "picking_id": picking.id,
                    "location_id": stock_location.id,
                    "location_dest_id": customer_location.id,
                }
            )
        return picking

    def put_in_pack(self, picking, packaging):
        wiz = self.env["choose.delivery.package"].create(
            {"picking_id": picking.id, "delivery_packaging_id": packaging.id}
        )
        picking.action_assign()
        wiz.put_in_pack()

    def _get_webservice(self):
        return PostlogisticsWebServiceDangerousGoods(self.company)

    @recorder.use_cassette
    def test_validate_wrong_unnumber(self):
        # Should raise an exception if unnumber is not a 4 digits long string
        products = [(self.product_lq_wrong_number, 10.0)]
        picking = self.create_picking(products)
        self.put_in_pack(picking, self.postlogistics_packaging)
        with self.assertRaises(exceptions.UserError):
            picking._generate_postlogistics_label()

    @recorder.use_cassette
    def test_confirm_right_unnumber(self):
        products = [(self.product_lq, 10.0)]
        picking = self.create_picking(products)
        self.put_in_pack(picking, self.postlogistics_packaging)
        picking._generate_postlogistics_label()

    def test_json_no_dangerous_goods(self):
        # When there's no dangerous goods in the package,
        # no unnumber should be sent through the api
        products = [(self.product_no_lq, 10.0)]
        picking = self.create_picking(products)
        self.put_in_pack(picking, self.postlogistics_packaging)
        package_ids = picking._get_packages_from_picking()
        webservice = self._get_webservice()
        recipient = webservice._prepare_recipient(picking)
        item_list = webservice._prepare_item_list(picking, recipient, package_ids)
        self.assertFalse(item_list[0]["attributes"].get("unnumbers"))

    def test_json_dangerous_goods(self):
        # When there's dangerous goods in the package,
        # we should have the list of unnumbers
        products = [(self.product_lq, 10.0)]
        picking = self.create_picking(products)
        self.put_in_pack(picking, self.postlogistics_packaging)
        package_ids = picking._get_packages_from_picking()
        webservice = self._get_webservice()
        recipient = webservice._prepare_recipient(picking)
        item_list = webservice._prepare_item_list(picking, recipient, package_ids)
        expected_unnumbers = [
            1234,
        ]
        self.assertEqual(item_list[0]["attributes"]["unnumbers"], expected_unnumbers)
