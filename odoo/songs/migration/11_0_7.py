# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.modules import uninstall


@anthem.log
def uninstall_account_bank_statement_import_camt(ctx):
    """ Uninstall account_bank_statement_import_camt """
    module_list = [
        'account_bank_statement_import_camt',
    ]
    uninstall(ctx, module_list)


@anthem.log
def pre(ctx):
    """ PRE 11.0.7: migration """
    uninstall_account_bank_statement_import_camt(ctx)
