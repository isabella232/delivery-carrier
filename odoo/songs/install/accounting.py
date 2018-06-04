# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def fix_invoice_company_group(ctx):
    """ Fix invoice company group """
    invoices = ctx.env['account.invoice'].search([])
    for invoice in invoices:
        invoice.onchange_partner_id()


@anthem.log
def main(ctx):
    """ Main: accounting """
    fix_invoice_company_group(ctx)
