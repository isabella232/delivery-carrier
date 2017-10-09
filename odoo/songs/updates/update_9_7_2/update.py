# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def remove_translation(ctx, module_name):
    """ remove translation """
    ctx.env['ir.translation'].search(
        [('module', '=', module_name)]
    ).unlink()


@anthem.log
def reload_translation(ctx, module_name):
    """ update translation """
    ctx.env['ir.module.module'].with_context(overwrite=True).search(
        [('name', '=', module_name)]
    ).update_translations()


@anthem.log
def main(ctx):
    """ Loading data """
    module_name = 'specific_reports'
    remove_translation(ctx, module_name)
    reload_translation(ctx, module_name)
