# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests.common import SavepointCase


class TestCalendarEvent(SavepointCase):

    def test_building_project_id(self):
        project = self.env['building.project'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest project'
            })
        lead = self.env['crm.lead'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest opportunity',
                'type': 'opportunity',
                'building_project_id': project.id
            })
        event = self.env['calendar.event'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest event',
                'opportunity_id': lead.id,
                'start': fields.Datetime.now(),
                'stop': fields.Datetime.now(),
            })

        self.assertEqual(project, event.building_project_id)

        # Change the lead building projecr
        project2 = self.env['building.project'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest other project'
            })

        lead.building_project_id = project2
        self.assertEqual(project2, event.building_project_id)

        # Remove opportunity on event
        event.opportunity_id = False
        self.assertFalse(event.building_project_id)
