# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_project_ids = fields.One2many(
        comodel_name='building.project',
        compute='_compute_building_projects',
        string='Bauprojekt',
    )

    @api.multi
    def get_company_partner(self):
        self.ensure_one()
        if self.parent_id:
            return self.parent_id
        else:
            return self

    @api.multi
    def _compute_building_projects(self):
        for rec in self:
            if rec.is_company:
                domain = [('partner_id', '=', rec.id)]
                recs = self.env['building.project.pricelist'].search(domain)
                rec.building_project_ids = recs.mapped('building_project_id')
