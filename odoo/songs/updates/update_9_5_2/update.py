# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem

@anthem.log
def set_report_base_url(ctx):
    """ Configuring web.base.url """
    url = 'http://localhost:8069'
    ctx.env['ir.config_parameter'].set_param('report.url', url)


@anthem.log
def main(ctx):
    """ Loading data """
    set_report_base_url(ctx)
