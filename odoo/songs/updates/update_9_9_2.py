# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def fix_report_domain(ctx):
    """ Fix report domains """
    vat_tag_302_a = ctx.env.ref('__setup__.vat_tag_302_a')
    vat_tag_342_a = ctx.env.ref('__setup__.vat_tag_342_a')
    vat_tag_302_b = ctx.env.ref('__setup__.vat_tag_302_b')
    vat_tag_342_b = ctx.env.ref('__setup__.vat_tag_342_b')

    frl_chtax_302_a = ctx.env.ref(
        '__setup__.financial_report_line_chtax_302_a'
    )
    frl_chtax_342_a = ctx.env.ref(
        '__setup__.financial_report_line_chtax_342_a'
    )
    frl_chtax_302_b = ctx.env.ref(
        '__setup__.financial_report_line_chtax_302_b'
    )
    frl_chtax_342_b = ctx.env.ref(
        '__setup__.financial_report_line_chtax_342_b'
    )

    frl_chtax_302_a.domain = "[('tax_ids.tag_ids', 'in', [{id}])]".format(
        id=vat_tag_302_a.id
    )
    frl_chtax_342_a.domain = "[('tax_ids.tag_ids', 'in', [{id}])]".format(
        id=vat_tag_342_a.id
    )
    frl_chtax_302_b.domain = "[('tax_line_id.tag_ids', 'in', [{id}])]".format(
        id=vat_tag_302_b.id
    )
    frl_chtax_342_b.domain = "[('tax_line_id.tag_ids', 'in', [{id}])]".format(
        id=vat_tag_342_b.id
    )


@anthem.log
def pre_update(ctx):
    """ fix VAT report """
    fix_report_domain(ctx)
