# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Swisslux Reports Customization',
    'summary': 'Layouts',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp',
    'maintainer': 'Camptocamp',
    'category': 'Reports',
    'complexity': "normal",  # easy, normal, expert
    'depends': [
        'account',
        'account_reports',
        'delivery',
        'mrp',
        'sale',
        'sale_stock',
        'stock',
        'swisslux_product',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        'views/invoice.xml',
        'views/layouts.xml',
        'views/sale.xml',
        'views/product.xml',
        'views/templates.xml',
        'views/company.xml',
        'views/report_inventory.xml',
        'views/report_invoice.xml',
        # TODO: Finish the migration of this report:
        # TODO: See the card https://jira.camptocamp.com/browse/BSSLX-76
        # 'views/report_mrporder.xml',
        'views/report_picking.xml',
        'views/report_purchase.xml',
        'views/report_sale.xml',
        'views/report_followup.xml',
        'views/report_stockinventory.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
