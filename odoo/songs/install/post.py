# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def admin_user_password(ctx):
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$12000$jpESopSSspZSihGCkFIKgQ$ERBXlRyOqRO0LTdpmamlO'
        'QFQnGMDKndQZaHRZfmvzYAeQWH/R6wv.QVnlj.cEV4/xshhEAdK8H7ro525hy.LjA'
    )


@anthem.log
def main(ctx):
    """ Main installation """
    admin_user_password(ctx)
