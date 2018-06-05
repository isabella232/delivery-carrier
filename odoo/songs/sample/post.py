# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update

from ..common import req
from base64 import b64encode
from pkg_resources import resource_string


@anthem.log
def setup_company(ctx):
    """ Setup company """
    logo_content = resource_string(req, 'data/images/company_logo.png')
    b64_logo = b64encode(logo_content)
    report_logo_content = resource_string(
          req, 'data/images/company_logo_header.png')
    b64_report_logo = b64encode(report_logo_content)

    ctx.env.ref('base.main_company').write({
        'logo': b64_logo,
        'report_logo': b64_report_logo,
    })

    # Main partner is updated in post instead of pre, else "Vendor Bills" and
    # "Customer Invoices" journals codes are not preserved.
    ctx.env.ref('base.main_partner').write({
        'name': "Swisslux AG",
        'street': "Industriestrasse 8",
        'zip': "8618",
        'city': "Oetwil am See",
        'country_id': ctx.env.ref('base.ch').id,
        'phone': "+41 43 844 80 80",
        'fax': "+41 43 844 80 81",
        'email': "info@swisslux.ch",
        'website': "http://www.swisslux.ch",
        'lang': 'de_DE',
        'logo': b64_logo,
        'company_id': ctx.env.ref('base.main_company').id,
    })

    values = {
        'name': "Swisslux SA",
        'street': "Chemin de la Grand Clos 17",
        'zip': "1092",
        'city': "Belmont-sur-Lausanne",
        'country_id': ctx.env.ref('base.ch').id,
        'phone': "+41 21 711 23 40",
        'fax': "+41 21 711 23 41",
        'email': "info@swisslux.ch",
        'website': "http://www.swisslux.ch",
        'lang': 'fr_FR',
        'logo': b64_logo,
        'company_id': ctx.env.ref('base.main_company').id,
        'parent_id': ctx.env.ref('base.main_partner').id,
    }
    create_or_update(ctx, 'res.partner',
                     '__setup__.partner_swisslux_romandie', values)


@anthem.log
def admin_user_password(ctx):
    """ Change admin password """
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$12000$jpESopSSspZSihGCkFIKgQ$ERBXlRyOqRO0LTdpmamlO'
        'QFQnGMDKndQZaHRZfmvzYAeQWH/R6wv.QVnlj.cEV4/xshhEAdK8H7ro525hy.LjA'
    )


@anthem.log
def set_product_uom_precision(ctx):
    uom_acc = ctx.env.ref('product.decimal_product_uom')
    uom_acc.digits = 1


@anthem.log
def main(ctx):
    """ Main installation """
    setup_company(ctx)
    admin_user_password(ctx)
    set_product_uom_precision(ctx)
