# Copyright 2015 Swisslux
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResPartnerRegion(models.Model):
    _name = 'res.partner.region'

    name = fields.Char("Gebietname", required=True)
