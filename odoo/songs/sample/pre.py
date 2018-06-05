# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR', 'de_DE', 'it_IT'):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([
        ('code', 'in', ['fr_FR', 'de_DE', 'it_IT']),
    ]).write({
        'grouping': [3, 0],
        'date_format': '%d.%m.%Y',
        'thousands_sep': "'",
        'decimal_point': '.',
    })


@anthem.log
def setup_company(ctx):
    """ Setup company """
    ctx.env.ref('base.main_company').write({
        'name': "Swisslux AG",
        'street': "Industriestrasse 8",
        'zip': "8618",
        'city': "Oetwil am See",
        'country_id': ctx.env.ref('base.ch').id,
        'phone': "+41 43 844 80 80",
        'fax': "+41 43 844 80 81",
        'email': "info@swisslux.ch",
        'website': "http://www.swisslux.ch",
        'vat': "CHE-107.897.036 MWST",
        'company_registry': "CHE-107.897.036",
        'rml_header1': '',
    })


@anthem.log
def set_address_format(ctx):
    address_format = (
        "%(street)s\n"
        "%(street2)s\n"
        "%(country_code)s-%(zip)s %(city)s"
    )
    ctx.env['res.country'].search([('code', 'like', 'CH')]).write({
        'address_format': address_format,
    })


@anthem.log
def main(ctx):
    """ Main: pre module install setup """
    setup_language(ctx)
    setup_company(ctx)
    set_address_format(ctx)
