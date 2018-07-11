# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ReportAllChannelsSales(models.Model):
    _inherit = "report.all.channels.sales"

    statistics_include = fields.Boolean(
        'Include in statistics', readonly=True
    )

    def get_main_request(self):
        request = super().get_main_request()
        return request.replace("product_qty",
                               "product_qty, statistics_include")

    def _select(self):
        return super()._select() \
            + ", s.statistics_include"

    def _group_by(self):
        return super()._group_by() + ", s.statistics_include"
