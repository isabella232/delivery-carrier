# Copyright 2017 Vincent Renaville (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Company Group",
    "summary": "Company Group for be able to get company discount analysis",
    "version": "11.0.1.0.0",
    "category": "Swisslux Modules",
    "website": "https://camptocamp.com",
    "author": "Camptocamp",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
        "account",
        "specific_partner",
        "specific_building_project"
    ],
    "data": [
        "views/res_partner.xml",
        "views/account_invoice.xml",
        "views/sale_order.xml",
        "reports/sale_report.xml",
        "reports/invoice_report.xml",

    ],
}
