# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date

from openerp import api, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class AccountReportContextFollowup(models.TransientModel):
    _inherit = 'account.report.context.followup'

    @api.multi
    def get_lang_today(self):
        """ Return the date of today in partner lang format.
        """
        self.ensure_one()
        code_lang = self.partner_id.lang or self.env.user.lang or 'en_US'
        lang = self.env['res.lang'].search([('code', '=', code_lang)], limit=1)
        return date.today().strftime(
            lang.date_format or DEFAULT_SERVER_DATE_FORMAT
        )
