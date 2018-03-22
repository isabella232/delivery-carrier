# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    substitute_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Substitute',
        track_visibility='onchange'
    )
