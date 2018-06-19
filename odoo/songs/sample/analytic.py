# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.settings import define_settings


@anthem.log
def set_analytic_settings(ctx):
    define_settings(ctx, 'res.config.settings', {
        'group_analytic_accounting': True,
        'group_analytic_account_for_purchases': True,
    })


@anthem.log
def main(ctx):
    """ Configuring analytic """
    set_analytic_settings(ctx)
