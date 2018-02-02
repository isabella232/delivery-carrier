# -*- coding: utf-8 -*-
# © 2016 Yannick Vaucher (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    receipt_checklist = fields.Text()

    cut_e_nr = fields.Char(
        compute="_compute_cut_e_nr",
        string='cut Enr',
        readonly=True
    )

    @api.one
    def _compute_cut_e_nr(self):
        line = self.e_nr or ''
        n = 3
        start_from_end = True
        if start_from_end:
            self.cut_e_nr = ' '.join([
                line[i-n if i-n >= 0 else 0:i] for i in range(len(line), 0, -n)
            ][::-1])
        else:
            self.cut_e_nr = ' '.join([
                line[i:i + n] for i in xrange(0, len(line), n)
            ])
