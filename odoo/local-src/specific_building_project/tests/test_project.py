# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestProject(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProject, cls).setUpClass()

        cls.department = cls.env['hr.department'].with_context(
            tracking_disable=True).create({
                'name': 'Test department',
            })

        # Delete existing employees for our user.
        employees = cls.env['hr.employee'].search([
            ('user_id', '=', cls.env.user.id)]
        )
        for employee in employees:
            cls.env['hr.attendance'].search([
                ('employee_id', '=', employee.id)]
            ).unlink()
            employee.unlink()

        cls.env['hr.employee'].with_context(tracking_disable=True).create({
            'name': 'Test employee',
            'user_id': cls.env.user.id,
            'department_id': cls.department.id
        })

    def test_department_id(self):
        project = self.env['project.project'].with_context(
            tracking_disable=True).create({
                'name': 'Unittest project',
            })

        self.assertEqual(self.env.user, project.user_id)

        project.onchange_user_id()
        self.assertEqual(self.department, project.department_id)
        self.assertEqual(
            self.department, project.analytic_account_id.department_id
        )
