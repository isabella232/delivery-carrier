# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Swisslux - Account',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Swisslux Modules',
    'website': 'http://www.swisslux.ch',
    'images': [],
    'depends': [
        'account',
        'account_payment_order',
    ],
    'data': [
        # Security
        'security/account_invoice.xml',
        # Views
        'views/account_invoice.xml',
        # Wizards
        'wizards/account_invoice_refund.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}
