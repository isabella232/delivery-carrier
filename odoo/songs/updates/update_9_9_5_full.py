# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def outgoing_mail_settings(ctx):
    """ Configure outgoing mail server """
    ir_mail_server = ctx.env['ir.mail_server']
    slx_0365 = ir_mail_server.search([('name', '=', 'SLX_O365')])
    if slx_0365:
        slx_0365.unlink()
    slx_vexc01 = ir_mail_server.search([('name', '=', 'SLX_VEXC01')])
    if not slx_vexc01:
        ir_mail_server.create({
            'name': 'SLX_VEXC01',
        })


@anthem.log
def post(ctx):
    """ Update 9.9.5 full: POST """
    outgoing_mail_settings(ctx)
