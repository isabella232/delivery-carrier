# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update

@anthem.log
def reload_translation(ctx, module):
    """ update translation """
    ctx.env['ir.module.module'].with_context(overwrite=True).search(
        [('name', '=', module)]).update_translations()


@anthem.log
def get_new_default_code(ctx):
    """ Update product default_code id (2793, 2792, 2785)"""
    all_duplicate_product = ctx.env['product.product'].search(
        [('id', 'in', (2793, 2792, 2785))])
    for product in all_duplicate_product:
        product.default_code = ctx.env['ir.sequence'].next_by_code(
            'product.product')


@anthem.log
def main(ctx):
    """ Loading data """
    get_new_default_code(ctx)
    reload_translation(ctx, 'specific_reports')
