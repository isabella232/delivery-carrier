# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.multi
    def get_employee_from_user(self):
        self.ensure_one()
        return self.employee_ids[0]
