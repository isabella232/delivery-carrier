# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def update_product_taxes(ctx):
    """update sale tax"""
    ctx.env.cr.execute("""
        UPDATE product_taxes_rel SET tax_id=84 WHERE tax_id=13;
    """)
    ctx.env.cr.execute("""
        UPDATE product_taxes_rel SET tax_id=85 WHERE tax_id=14;
    """)
    """update purchase tax"""
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=91 WHERE tax_id=12;
    """)
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=92 WHERE tax_id=17;
    """)
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=88 WHERE tax_id=15;
    """)
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=93 WHERE tax_id=18;
    """)
    ctx.env.cr.execute("""
        UPDATE product_supplier_taxes_rel SET tax_id=89 WHERE tax_id=16;
    """)


@anthem.log
def pre_update(ctx):
    """update product with new taxes"""
    update_product_taxes(ctx)
