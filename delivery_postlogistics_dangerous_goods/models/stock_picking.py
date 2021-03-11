# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models

from ..postlogistics.web_service import PostlogisticsWebServiceDangerousGoods


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _generate_postlogistics_label(self, webservice_class=None, package_ids=None):
        """ Generate post logistic label using specific from this module."""
        return super()._generate_postlogistics_label(
            webservice_class=PostlogisticsWebServiceDangerousGoods,
            package_ids=package_ids,
        )
