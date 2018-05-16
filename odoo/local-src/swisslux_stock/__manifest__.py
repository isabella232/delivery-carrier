# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Swisslux - Stock',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Swisslux Modules',
    'website': 'http://www.swisslux.ch',
    'images': [],
    'depends': [
        'stock_split_picking',
        'delivery'
    ],
    'data': [
        'report/stock_inventory.xml',
        'views/stock_inventory.xml',
        'views/stock_picking.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}
