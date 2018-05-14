# Copyright 2015-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    report_logo = fields.Binary(
        help='Logo shown in reports',
    )

    receipt_checklist = fields.Text()
