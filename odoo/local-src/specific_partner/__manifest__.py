# Copyright 2015 Swisslux
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Specific - Partner',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Swisslux Modules',
    'website': 'http://www.swisslux.ch',
    'depends': [
        'account',
        'crm',
        'sale',
        'l10n_ch_zip'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/partner_title.xml',
        'views/better_zip.xml',
        'data/sequence.xml',
    ],
}
