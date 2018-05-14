# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def get_employee_from_user(self, user_id=None):
        so = self.env['sale.order'].search([('name', '=', self.origin)])
        if not so and not user_id:
            user_id = self.partner_id.user_id
        elif not user_id:
            user_id = so.user_id

        if user_id:
            hr_employee = so.get_employee_from_user(user_id)
        else:
            hr_employee = False

        return hr_employee
