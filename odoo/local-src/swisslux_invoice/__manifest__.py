# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Swisslux - Invoice',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Swisslux Modules',
    'website': 'http://www.swisslux.ch',
    'images': [],
    'depends': [
        'account',
        'l10n_ch_base_bank',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/invoice_bank_rule.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}
