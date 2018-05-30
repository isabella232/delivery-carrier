# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def get_employee_from_user(self, user_id):
        self.ensure_one()
        resource = self.env['resource.resource'].search(
            [('user_id', '=', user_id.id)])
        hr_employee = self.env['hr.employee'].search(
            [('resource_id', '=', resource.id)])

        return hr_employee
