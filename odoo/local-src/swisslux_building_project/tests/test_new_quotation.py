# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestNewQuotation(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestNewQuotation, cls).setUpClass()

        cls.partner = cls.env['res.partner'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest partner'
            })
        cls.building_project = cls.env['building.project'].with_context(
            tracking_disable=True).create({
                'name': 'Building Project',
            })
        cls.opportunity = cls.env['crm.lead'].with_context(
            tracking_disable=True).create({
                'name': 'Opportunity',
                'partner_id': cls.partner.id,
            })

    def test_new_quotation_with_building_project(self):
        self.opportunity.building_project_id = self.building_project
        res = self.opportunity.with_context(
            default_building_project_id=self.building_project.id
        ).create_new_quotation()

        project_id = res['context'].get('default_project_id')
        partner_id = res['context'].get('default_partner_id')

        self.assertEqual(
            project_id, self.building_project.analytic_account_id.id
        )
        self.assertEqual(partner_id, self.partner.id)

    def test_new_quotation_standard(self):
        res = self.opportunity.create_new_quotation()
        project_id = res['context'].get('default_project_id')
        partner_id = res['context'].get('default_partner_id')
        self.assertFalse(project_id)
        self.assertEqual(partner_id, self.partner.id)
