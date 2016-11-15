# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def reload_translation(ctx, module):
    """ update translation """
    ctx.env['ir.module.module'].with_context(overwrite=True).search(
        [('name', '=', module)]).update_translations()


@anthem.log
def main(ctx):
    """ Loading data """
    reload_translation(ctx, 'specific_reports')
