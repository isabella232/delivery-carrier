# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update
from ..common import load_csv_no_tracking


@anthem.log
def remove_default_payment_term(ctx):
    ctx.env.ref('account.account_payment_term_15days').unlink()
    ctx.env.ref('account.account_payment_term_net').unlink()
    ctx.env.ref('account.account_payment_term_immediate').unlink()


@anthem.log
def import_payment_term(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/account.payment.term.csv', 'account.payment.term')


@anthem.log
def remove_demo_followup(ctx):
    ctx.env.ref('account_reports_followup.demo_followup1').unlink()


@anthem.log
def create_followup(ctx):
    values = {
        'company_id': ctx.env.ref('base.main_company').id,
    }
    create_or_update(ctx, 'account_followup.followup',
                     '__setup__.followup_1', values)

    records = [
        {'xmlid': '__setup__.followup_1_line_1',
         'name': '1. Mahnung',
         'followup_id': ctx.env.ref('__setup__.followup_1').id,
         'sequence': 1,
         'delay': 20,
         'send_email': False,
         },
        {'xmlid': '__setup__.followup_1_line_2',
         'name': '2. Mahnung',
         'followup_id': ctx.env.ref('__setup__.followup_1').id,
         'sequence': 2,
         'delay': 35,
         'send_email': False,
         'description': 'STHOESUTHOE',
         },
        {'xmlid': '__setup__.followup_1_line_3',
         'name': '3. Mahnung',
         'followup_id': ctx.env.ref('__setup__.followup_1').id,
         'sequence': 3,
         'delay': 45,
         'send_email': False,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'account_followup.followup.line', xmlid, record)


@anthem.log
def main(ctx):
    """ Configuring follow-ups """
    remove_default_payment_term(ctx)
    import_payment_term(ctx)
    remove_demo_followup(ctx)
    create_followup(ctx)
