# -*- coding: utf-8 -*-
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from openerp import api, models, _
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

    def get_pdf(self, log=False):
        """Override to manage header footer context"""
        bodies = []
        headers = []
        footers = []
        for context in self:
            context = context.with_context(lang=context.partner_id.lang)
            report_obj = context.get_report_obj()
            lines = report_obj.get_lines(context, public=True)
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
            rcontext = {
                'context': context,
                'report': report_obj,
                'lines': lines,
                'mode': 'print',
                'base_url': base_url,
                'css': '',
                'o': self.env.user,
                'today': context._formatLangDate(datetime.today()),
                'company': self.env.user.company_id,
                'res_company': self.env.user.company_id,
                'tpl_partners_only': True,
            }
            html = self.pool['ir.ui.view'].render(
                self._cr, self._uid,
                report_obj.get_template() + '_letter',
                rcontext, context=context.env.context
            )
            bodies.append((0, html))
            footer = self.pool['ir.ui.view'].render(
                self._cr, self._uid,
                "report.external_layout_footer",
                rcontext,
                context=self.env.context
            )
            rcontext['subst'] = True
            rcontext['body'] = footer
            rcontext[0] = footer
            footer = self.pool['ir.ui.view'].render(
                self._cr, self._uid,
                "report.minimal_layout",
                rcontext,
                context=self.env.context)
            footers.append(footer)
            if log:
                msg = _('Sent a followup leter')
                context.partner_id.message_post(
                    body=msg,
                    subtype='account_reports.followup_logged_action'
                )

        return self.env['report']._run_wkhtmltopdf(
            headers,
            footers,
            bodies,
            False,
            self.env.user.company_id.paperformat_id
        )
