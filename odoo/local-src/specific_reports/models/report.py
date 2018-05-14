# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        """ Don't save attachment if the report is generated for email.
        """
        if 'default_template_id' in self.env.context:
            save_in_attachment = False
        return super()._post_pdf(save_in_attachment, pdf_content, res_ids)
