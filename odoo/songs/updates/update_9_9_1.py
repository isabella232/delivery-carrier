# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def update_product_taxes(ctx):
    """update sale tax"""
    tax_sale_8_excl_id = ctx.env['account.tax'].search([
        ('amount', '=', 8.0), ('type_tax_use', '=', 'sale'),
        ('price_include', '=', False)]).id
    tax_sale_8_incl_id = ctx.env['account.tax'].search([
        ('amount', '=', 8.0), ('type_tax_use', '=', 'sale'),
        ('price_include', '=', True)]).id
    tax_sale_77_excl_id = ctx.env.ref('__setup__.vat_7_7_sales_excl').id
    tax_sale_77_incl_id = ctx.env.ref('__setup__.vat_7_7_sales_incl').id

    ctx.env.cr.execute("""
        UPDATE product_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_sale_77_excl_id, tax_sale_8_excl_id))
    ctx.env.cr.execute("""
        UPDATE product_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_sale_77_incl_id, tax_sale_8_incl_id))

    """update purchase tax"""
    tax_invest_38_incl_id = ctx.env['account.tax'].search([
        ('amount', '=', 3.8), ('type_tax_use', '=', 'purchase'),
        ('price_include', '=', True), ('description', 'ilike', 'invest')]).id
    tax_invest_8_excl_id = ctx.env['account.tax'].search([
        ('amount', '=', 8.0), ('type_tax_use', '=', 'purchase'),
        ('price_include', '=', False), ('description', 'ilike', 'invest')]).id
    tax_purchase_8_excl_id = ctx.env['account.tax'].search([
        ('amount', '=', 8.0), ('type_tax_use', '=', 'purchase'),
        ('price_include', '=', False), ('description', 'ilike', 'achat')]).id
    tax_invest_8_incl_id = ctx.env['account.tax'].search([
        ('amount', '=', 8.0), ('type_tax_use', '=', 'purchase'),
        ('price_include', '=', True), ('description', 'ilike', 'invest')]).id
    tax_purchase_8_incl_id = ctx.env['account.tax'].search([
        ('amount', '=', 8.0), ('type_tax_use', '=', 'purchase'),
        ('price_include', '=', True), ('description', 'ilike', 'achat')]).id
    tax_invest_37_incl_id = ctx.env.ref('__setup__.vat_3_7_sales_incl').id
    tax_invest_77_excl_id = ctx.env.ref('__setup__.vat_7_7_invest_excl').id
    tax_purchase_77_excl_id = ctx.env.ref('__setup__.vat_7_7_purchase_excl').id
    tax_invest_77_incl_id = ctx.env.ref('__setup__.vat_7_7_invest_incl').id
    tax_purchase_77_incl_id = ctx.env.ref('__setup__.vat_7_7_purchase_incl').id

    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_invest_37_incl_id, tax_invest_38_incl_id))
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_invest_77_excl_id, tax_invest_8_excl_id))
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_purchase_77_excl_id, tax_purchase_8_excl_id))
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_invest_77_incl_id, tax_invest_8_incl_id))
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=%s WHERE tax_id=%s;
    """, (tax_purchase_77_incl_id, tax_purchase_8_incl_id))


@anthem.log
def pre_update(ctx):
    """update product with new taxes"""
    update_product_taxes(ctx)
