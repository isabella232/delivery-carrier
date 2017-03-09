# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def get_new_default_code(ctx):
    """ Update product default_code id (2802, 2803, 2820)"""
    all_duplicate_product = ctx.env['product.product'].search(
        [('id', 'in', (2802, 2803, 2820))])
    for product in all_duplicate_product:
        product.default_code = ctx.env['ir.sequence'].next_by_code(
            'product.product')


@anthem.log
def main(ctx):
    """ Loading data """
    get_new_default_code(ctx)
