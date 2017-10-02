# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def outgoing_mail_settings(ctx):
    """ Configure outgoing mail server """
    ir_mail_server = ctx.env['ir.mail_server']
    slx = ir_mail_server.search([('name', '=', 'SLX_TEST')])
    if not slx:
        ir_mail_server.create({
            'name': 'SLX_TEST',
        })


@anthem.log
def main(ctx):
    """ Loading data """
    outgoing_mail_settings(ctx)
