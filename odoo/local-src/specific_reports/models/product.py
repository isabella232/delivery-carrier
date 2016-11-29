# -*- coding: utf-8 -*-
# © 2016 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    receipt_checklist = fields.Text()

    cut_e_nr = fields.Char(
        compute="_compute_cut_enr",
        string='cut Enr',
        readonly=True
    )

    @api.one
    def _compute_cut_enr(self):
        self.cut_e_nr = ' '.join(self.e_nr[i:i + 3] for i in xrange(
            0, len(self.e_nr), 3))
