# © 2016 Cyril Gaudin (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from lxml import etree


class ProjectProject(models.Model):
    _inherit = 'project.project'

    building_template = fields.Boolean(default=False)

    building_project_id = fields.Many2one(
        comodel_name='building.project',
        compute='_compute_building_project_id'
    )

    @api.multi
    def _compute_building_project_id(self):
        building_obj = self.env['building.project']
        for record in self:
            record.building_project_id = building_obj.search(
                [('project_id', '=', record.id)],
                limit=1
            )[:1]

    def init(self):
        self.env.cr.execute(
            'SELECT indexname FROM pg_indexes WHERE indexname = %s',
            ('project_project_idx_unique_building_template',)
        )
        if not self.env.cr.fetchone():
            self.env.cr.execute(
                'CREATE UNIQUE INDEX '
                'project_project_idx_unique_building_template '
                'ON project_project (building_template) '
                'WHERE building_template'
            )

    @api.onchange('user_id')
    def onchange_user_id(self):
        """ Set department_id to user_id.department_id if empty
        """
        if not self.department_id:
            self.department_id = self.user_id.department_id

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        """ Modify search view to add a filter on connected user department.
        """
        result = super().fields_view_get(view_id, view_type, toolbar, submenu)
        user = self.env.user
        if view_type == 'search':
            eview = etree.fromstring(result['arch'])
            nodes = eview.xpath("//filter[@name='department']")
            if nodes:
                if user.department_id:
                    nodes[0].set(
                        'domain',
                        "['|', ('department_id', 'child_of', [%s]), "
                        "('department_id', 'parent_of', [%s])]"
                        % (user.department_id.id, user.department_id.id)
                    )
                else:
                    eview.remove(nodes[0])
            result['arch'] = etree.tostring(eview)

        return result
