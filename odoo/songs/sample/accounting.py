# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update
from anthem.lyrics.settings import define_settings
from ..common import load_csv_no_tracking


@anthem.log
def set_currencies(ctx):
    main_company = ctx.env.ref('base.main_company')
    main_company.currency_id = ctx.env.ref('base.CHF').id

    define_settings(ctx, 'res.config.settings', {
        'group_multi_currency': True,
    })

    ctx.env.ref('base.HKD').write({
       'active': True,
    })


@anthem.log
def remove_cash_bank(ctx):
    ctx.env['account.account'].search([
        ('name', 'in', ['Cash', 'Bank']),
    ]).unlink()
    ctx.env['account.journal'].search([
        ('name', 'in', ['Cash', 'Bank']),
    ]).unlink()


@anthem.log
def account_chart_extended(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/account.account.csv', 'account.account')


@anthem.log
def create_bank_accounts(ctx):
    expense_type = ctx.env.ref('account.data_account_type_expenses')
    records = [
        {'xmlid': '__setup__.account_1010',
         'name': 'CCP 84-001285-1',
         'code': '1010',
         'user_type_id': expense_type.id,
         },
        {'xmlid': '__setup__.account_1020',
         'name': 'ZKB CH7400700115500086877',
         'code': '1020',
         'user_type_id': expense_type.id,
         },
        {'xmlid': '__setup__.account_1021',
         'name': 'ZKB CH2300700115500179557',
         'code': '1021',
         'user_type_id': expense_type.id,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account.account', xmlid, record)


@anthem.log
def set_banks(ctx):
    create_or_update(ctx, 'res.bank', 'l10n_ch_bank.bank_730_0000', {
        'ccp': '01-200027-2'
    })

    main_company = ctx.env.ref('base.main_company')
    main_partner = ctx.env.ref('base.main_partner')

    records = [
        {'xmlid': '__setup__.bank_1',
         'partner_id': main_partner.id,
         'bank_id': ctx.env.ref('l10n_ch_bank.bank_9000_0000').id,
         'company_id': main_company.id,
         'acc_number': '84-001285-1',
         },
        {'xmlid': '__setup__.bank_2',
         'partner_id': main_partner.id,
         'bank_id': ctx.env.ref('l10n_ch_bank.bank_730_0000').id,
         'company_id': main_company.id,
         'acc_number': 'CH74 0070 0115 5000 8687 7',
         },
        {'xmlid': '__setup__.bank_3',
         'partner_id': main_partner.id,
         'bank_id': ctx.env.ref('l10n_ch_bank.bank_730_0000').id,
         'company_id': main_company.id,
         'acc_number': 'CH23 0070 0115 5001 7955 7',
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'res.partner.bank', xmlid, record)

    # FIXME: print_* fields were added by module l10n_ch_payment_slip
    # which is no longer used => how should it be replaced?
    create_or_update(ctx, 'res.partner.bank', '__setup__.bank_2', {
        'isr_adherent_num': 933421,
        # 'print_bank': True,
        # 'print_account': True,
        # 'print_partner': True,
    })

    accounts = {}
    for account in ctx.env['account.account'].search([
        ('code', 'in', ['1010', '1020', '1021']),
    ]):
        accounts[account.code] = account

    records = [
        {'xmlid': '__setup__.journal_POCH',
         'name': 'Postfinance',
         'code': 'POCH',
         'type': 'bank',
         'company_id': main_company.id,
         'currency_id': False,
         'default_debit_account_id': accounts['1010'].id,
         'default_credit_account_id': accounts['1010'].id,
         'update_posted': True,
         'bank_account_id': ctx.env.ref('__setup__.bank_1').id,
         },
        {'xmlid': '__setup__.journal_ZKB1',
         'name': 'ZKB (ES)',
         'code': 'BNK1',
         'type': 'bank',
         'company_id': main_company.id,
         'currency_id': False,
         'default_debit_account_id': accounts['1020'].id,
         'default_credit_account_id': accounts['1020'].id,
         'update_posted': True,
         'bank_account_id': ctx.env.ref('__setup__.bank_2').id,
         },
        {'xmlid': '__setup__.journal_ZKB2',
         'name': 'ZKB',
         'code': 'BNK2',
         'type': 'bank',
         'company_id': main_company.id,
         'currency_id': False,
         'default_debit_account_id': accounts['1021'].id,
         'default_credit_account_id': accounts['1021'].id,
         'update_posted': True,
         'bank_account_id': ctx.env.ref('__setup__.bank_3').id,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account.journal', xmlid, record)


@anthem.log
def set_bank_invoice(ctx):
    create_or_update(
        ctx, 'invoice.bank.rule',
        '__setup__.invoice_bank_rule_swiss', {
            'name': 'Bank for swiss customers',
            'partner_bank_id': ctx.env.ref('__setup__.bank_2').id,
            'country_id': ctx.env.ref('base.ch').id,
            'company_id': ctx.env.ref('base.main_company').id,
        })


@anthem.log
def set_journal(ctx):
    main_company = ctx.env.ref('base.main_company')
    account1024 = ctx.env['account.account'].search([
        ('code', '=', '1024'),
    ], limit=1)
    records = [
        {'xmlid': '__setup__.expense_journal',
         'name': 'Expenses',
         'code': 'EXP',
         'type': 'purchase',
         'company_id': main_company.id,
         'currency_id': False,
         'update_posted': True,
         'show_on_dashboard': True,
         'default_debit_account_id': False,
         'default_credit_account_id': False,
         },
        {'xmlid': '__setup__.wage_journal',
         'name': 'Wage',
         'code': 'WAGE',
         'type': 'purchase',
         'company_id': main_company.id,
         'currency_id': False,
         'update_posted': True,
         'show_on_dashboard': True,
         'default_debit_account_id': False,
         'default_credit_account_id': False,
         },
        {'xmlid': '__setup__.vendor_usd',
         'name': 'Vendor USD',
         'code': 'VUSD',
         'type': 'purchase',
         'company_id': main_company.id,
         'currency_id': ctx.env.ref('base.USD').id,
         'update_posted': True,
         'show_on_dashboard': True,
         'default_debit_account_id': False,
         'default_credit_account_id': False,
         },
        {'xmlid': '__setup__.vendor_eur',
         'name': 'Vendor EUR',
         'code': 'VEUR',
         'type': 'purchase',
         'company_id': main_company.id,
         'currency_id': ctx.env.ref('base.EUR').id,
         'update_posted': True,
         'show_on_dashboard': True,
         'default_debit_account_id': False,
         'default_credit_account_id': False,
         },
        {'xmlid': '__setup__.afex',
         'name': 'AFEX',
         'code': 'AFEX',
         'type': 'bank',
         'company_id': main_company.id,
         'currency_id': False,
         'update_posted': True,
         'show_on_dashboard': True,
         'default_debit_account_id': account1024.id,
         'default_credit_account_id': account1024.id,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account.journal', xmlid, record)


def _set_default_account_property(ctx, record, company):
    # Ported from
    # https://github.com/camptocamp/oerpscenario/blob/f663be2c161ebb4da93cd0c860073620155e9c4d/features/steps/dsl_helpers.py#L180-L201
    # and
    # https://github.com/camptocamp/oerpscenario/blob/f663be2c161ebb4da93cd0c860073620155e9c4d/features/steps/dsl.py#L122-L136
    fieldname = record['name']
    modelname = record['model']
    field = ctx.env['ir.model.fields'].search([
        ('name', '=', fieldname), ('model', '=', modelname)
    ])
    if not field:
        return
    ir_property = ctx.env['ir.property'].search([
        ('name', '=', fieldname),
        ('fields_id', '=', field.id),
        ('res_id', '=', False),
        ('company_id', '=', company.id),
    ])
    if ir_property is None:
        ctx.env['ir.property'].create({
            'fields_id': field.id,
            'name': fieldname,
            'res_id': False,
            'type': 'many2one',
            'company_id': company.id,
        })
    domain = [
        ('code', '=', record['account_code']),
        ('company_id', '=', company.id),
    ]
    model = ctx.env['account.account']
    res = model.search(domain)
    if res:
        ir_property.write({'value_reference': '%s,%s' % (modelname, res.id)})


@anthem.log
def set_default_accounts(ctx):
    main_company = ctx.env.ref('base.main_company')
    records = [
        {'name': 'property_account_receivable_id',
         'model': 'res.partner',
         'account_code': '1100',
         },
        {'name': 'property_account_payable_id',
         'model': 'res.partner',
         'account_code': '2000',
         },
        {'name': 'property_account_expense_categ_id',
         'model': 'product.category',
         'account_code': '4200',
         },
        {'name': 'property_account_income_categ_id',
         'model': 'product.category',
         'account_code': '3200',
         },
        {'name': 'property_stock_valuation_account_id',
         'model': 'product.category',
         'account_code': '1260',
         },
        {'name': 'property_stock_account_input',
         'model': 'product.template',
         'account_code': '1260',
         },
        {'name': 'property_stock_account_output',
         'model': 'product.template',
         'account_code': '1260',
         },
    ]
    for record in records:
        _set_default_account_property(ctx, record, main_company)

    ctx.env['ir.property'].search([
        ('name', '=', 'property_account_expense_id'),
        ('res_id', '=', False),
    ]).unlink()
    ctx.env['ir.property'].search([
        ('name', '=', 'property_account_income_id'),
        ('res_id', '=', False),
    ]).unlink()


@anthem.log
def set_bvr(ctx):
    # FIXME: all attributes below were added by module l10n_ch_payment_slip
    # which is no longer used => should they be replaced by something else?
    # The function is disabled in the meantime, see main()
    create_or_update(ctx, 'res.company', 'base.main_company', {
        'bvr_delta_horz': 0,
        'bvr_delta_vert': 0,
        'bvr_scan_line_horz': 0,
        'bvr_scan_line_vert': 0,
        'bvr_scan_line_font_size': 11,
        'bvr_scan_line_letter_spacing': 2.55,
        'bvr_add_horz': 0.1,
        'bvr_add_vert': 0,
        'bvr_background': True,
        'merge_mode': 'in_memory',
    })


@anthem.log
def set_account_cancel(ctx):
    ctx.env['account.journal'].search([
        ('code', 'in', ['INV', 'BILL', 'MISC', 'EXCH', 'STJ']),
    ]).write({
        'update_posted': True,
    })


@anthem.log
def configure_sepa(ctx):
    method = ctx.env.ref(
        'account_banking_sepa_credit_transfer.sepa_credit_transfer')
    method.write({
            'pain_version': 'pain.001.001.03.ch.02',
        })

    default_journal_ids = [
        ctx.env.ref('__setup__.expense_journal').id,
        ctx.env.ref('__setup__.wage_journal').id,
    ]
    vendorbills = ctx.env['account.journal'].search([
        ('code', '=', 'BILL'),
    ], limit=1)
    if vendorbills:
        default_journal_ids.append(vendorbills.id)

    create_or_update(
        ctx, 'account.payment.mode', '__setup__.account_payment_mode_1', {
            'name': 'SEPA (ZKB)',
            'active': True,
            'no_debit_before_maturity': False,
            'fixed_journal_id': ctx.env.ref('__setup__.journal_ZKB1').id,
            'generate_move': True,
            'group_lines': True,
            'default_journal_ids': [(6, False, default_journal_ids)],
            'bank_account_link': 'fixed',
            'default_invoice': False,
            'move_option': 'date',
            'offsetting_account': 'bank_account',
            'payment_method_id': method.id,
            'default_payment_mode': 'same',
            'payment_order_ok': True,
            'default_target_move': 'posted',
            'default_date_type': 'due',
        })


@anthem.log
def main(ctx):
    """ Configuring accounting """
    set_currencies(ctx)
    remove_cash_bank(ctx)
    account_chart_extended(ctx)
    create_bank_accounts(ctx)
    set_banks(ctx)
    set_bank_invoice(ctx)
    set_journal(ctx)
    set_default_accounts(ctx)
    # set_bvr(ctx)
    set_account_cancel(ctx)
    configure_sepa(ctx)
