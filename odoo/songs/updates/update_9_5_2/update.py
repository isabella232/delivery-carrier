# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem

@anthem.log
def set_web_base_url(ctx):
    """ Configuring web.base.url """
    url = 'http://localhost:8069'
    ctx.env['ir.config_parameter'].set_param('web.base.url', url)
    ctx.env['ir.config_parameter'].set_param('web.base.url.freeze', 'True')


@anthem.log
def main(ctx):
    """ Loading data """
    set_web_base_url(ctx)
