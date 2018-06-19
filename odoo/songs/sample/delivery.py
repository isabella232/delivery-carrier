# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def configure_postlogistics_authentification(ctx):
    options = {}
    for option in ctx.env['delivery.carrier.template.option'].search([
        ('code', 'in', ['A7', 'PDF', '300']),
    ]):
        options[option.code] = option
    values = {
        'postlogistics_username': 'TUW003693',
        'postlogistics_password': '8cB{0tHf))C%',
        'postlogistics_office': '',
        'postlogistics_default_label_layout': option['A7'].id,
        'postlogistics_default_output_format': option['PDF'].id,
        'postlogistics_default_resolution': option['300'].id,
    }
    create_or_update(ctx, 'res.company',
                     'base.main_company', values)


@anthem.log
def configure_postlogistics_frankling_licenses(ctx):
    main_company = ctx.env.ref('base.main_company')
    records = [
        {'xmlid': '__setup__.postlogistics_license1',
         'name': 'Versand von Paketen',
         'number': '42133507',
         'company_id': main_company.id,
         'sequence': 1,
         },
        {'xmlid': '__setup__.postlogistics_license2',
         'name': 'Promo Sendungen',
         'number': '60004890',
         'company_id': main_company.id,
         'sequence': 2,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'postlogistics.license', xmlid, record)


@anthem.log
def update_postlogistics_services(ctx):
    # https://github.com/camptocamp/swisslux_odoo/blob/master/odoo/features/steps/delivery.py
    company = ctx.env.ref('base.main_company')
    label_layout = company.postlogistics_default_label_layout
    output_format = company.postlogistics_default_output_format
    resolution = company.postlogistics_default_resolution
    conf_wizard = ctx.env['postlogistics.config.settings'].create({
        'company_id': company.id,
    })
    vals = {
        'username': company.postlogistics_username,
        'password': company.postlogistics_password,
        'logo': company.postlogistics_logo,
        'office': company.postlogistics_office,
        'default_label_layout': label_layout,
        'default_output_format': output_format,
        'default_resolution': resolution,
    }
    conf_wizard.write(vals)
    conf_wizard.update_postlogistics_options()


@anthem.log
def add_delivery_method_for_postlogistics(ctx):
    postlogistics = ctx.env.ref(
        'delivery_carrier_label_postlogistics.postlogistics')

    groups = {}
    for group in ctx.env['postlogistics.service.group'].search([
        ('name', 'in', ['Parcel', 'Swiss-Express / Swiss-Courier']),
    ]):
        groups[group.name] = group
    parcel_group = groups['Parcel']
    express_group = groups['Swiss-Express / Swiss-Courier']

    license1 = ctx.env.ref('__setup__.postlogistics_license1')
    license2 = ctx.env.ref('__setup__.postlogistics_license2')

    records = [
        {'xmlid': '__setup__.carrier_post_eco',
         'name': 'Post Economy',
         'carrier_type': 'postlogistics',
         'partner_id': postlogistics.id,
         'postlogistics_service_group_id': parcel_group.id,
         'postlogistics_license_id': license1.id,
         'fixed_price': 0,
         },
        {'xmlid': '__setup__.carrier_post_pri',
         'name': 'Post Priority',
         'carrier_type': 'postlogistics',
         'partner_id': postlogistics.id,
         'postlogistics_service_group_id': parcel_group.id,
         'postlogistics_license_id': license1.id,
         'fixed_price': 0,
         },
        {'xmlid': '__setup__.carrier_post_pri200',
         'name': 'Post Priority 200',
         'carrier_type': 'postlogistics',
         'partner_id': postlogistics.id,
         'postlogistics_service_group_id': parcel_group.id,
         'postlogistics_license_id': license1.id,
         'fixed_price': 0,
         },
        {'xmlid': '__setup__.carrier_post_moon',
         'name': 'Post Express Mond',
         'carrier_type': 'postlogistics',
         'partner_id': postlogistics.id,
         'postlogistics_service_group_id': express_group.id,
         'postlogistics_license_id': license1.id,
         'fixed_price': 0,
         },
        {'xmlid': '__setup__.carrier_post_lighting',
         'name': 'Post Express Blitz',
         'carrier_type': 'postlogistics',
         'partner_id': postlogistics.id,
         'postlogistics_service_group_id': express_group.id,
         'postlogistics_license_id': license1.id,
         'fixed_price': 0,
         },
        {'xmlid': '__setup__.carrier_post_promo',
         'name': 'PostPac Promo',
         'carrier_type': 'postlogistics',
         'partner_id': postlogistics.id,
         'postlogistics_service_group_id': parcel_group.id,
         'postlogistics_license_id': license2.id,
         'fixed_price': 0,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'delivery.carrier', xmlid, record)


@anthem.log
def setup_postlogistics_carrier_options(ctx):
    options = {}
    for option in ctx.env['delivery.carrier.template.option'].search([
        ('name', 'in', ['ECO', 'PRI', 'SEM', 'SKB']),
    ]):
        options[option.code] = option
    records = [
        {'xmlid': '__setup__.carrier_option_post_eco_1',
         'carrier_id': ctx.env.ref('__setup__.carrier_post_eco').id,
         'tmpl_option_id': options['ECO'],
         'mandatory': True,
         'by_default': True,
         },
        {'xmlid': '__setup__.carrier_option_post_pri_1',
         'carrier_id': ctx.env.ref('__setup__.carrier_post_pri').id,
         'tmpl_option_id': options['PRI'],
         'mandatory': True,
         'by_default': True,
         },
        {'xmlid': '__setup__.carrier_option_post_pri_2',
         'carrier_id': ctx.env.ref('__setup__.carrier_post_pri200').id,
         'tmpl_option_id': options['PRI'],
         'mandatory': True,
         'by_default': True,
         },
        {'xmlid': '__setup__.carrier_option_post_moon_1',
         'carrier_id': ctx.env.ref('__setup__.carrier_post_moon').id,
         'tmpl_option_id': options['SEM'],
         'mandatory': True,
         'by_default': True,
         },
        {'xmlid': '__setup__.carrier_option_post_lighting_1',
         'carrier_id': ctx.env.ref('__setup__.carrier_post_lighting').id,
         'tmpl_option_id': options['SKB'],
         'mandatory': True,
         'by_default': True,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'delivery.carrier.option', xmlid, record)


@anthem.log
def create_ups_partner(ctx):
    create_or_update(ctx, 'res.partner', '__setup__.partner_ups', {
        'name': 'UPS'
    })


@anthem.log
def create_delivery_method(ctx):
    # FIXME IntegrityError: null value in column "product_id" violates
    # not-null constraint
    ups = ctx.env.ref('__setup__.partner_ups')
    main_partner = ctx.env.ref('base.main_partner')
    records = [
        {'xmlid': '__setup__.carrier_ups_express',
         'name': 'UPS Express',
         'partner_id': ups.id
         },
        {'xmlid': '__setup__.carrier_ups_express_plus',
         'name': 'UPS Express Plus',
         'partner_id': ups.id
         },
        {'xmlid': '__setup__.carrier_ups_express_saver',
         'name': 'UPS Express Saver',
         'partner_id': ups.id
         },
        {'xmlid': '__setup__.carrier_slx_take_away',
         'name': 'Abgeholt',
         'partner_id': main_partner.id
         },
        {'xmlid': '__setup__.carrier_slx_brought',
         'name': 'Überbracht',
         'partner_id': main_partner.id
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'delivery.carrier', xmlid, record)


@anthem.log
def main(ctx):
    """ Configuring deliveries """
    # FIXME postlogistics attributes and tables are missing.
    # They come from an OCA module whose migration to v11 is WIP:
    # https://github.com/OCA/delivery-carrier/pull/155
    # https://jira.camptocamp.com/browse/BSSLX-36

    # TODO Enable and test the following songs when PR is ready:
    # configure_postlogistics_authentification(ctx)
    # configure_postlogistics_frankling_licenses(ctx)
    # update_postlogistics_services(ctx)
    # add_delivery_method_for_postlogistics(ctx)
    # setup_postlogistics_carrier_options(ctx)
    create_ups_partner(ctx)
    # create_delivery_method(ctx)
