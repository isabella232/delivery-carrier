# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "HR extension",
    "summary": "Some HR extensions",
    "version": "11.0.0.0.0",
    "category": "HR",
    "website": "https://odoo-community.org/",
    "author": "Camptocamp",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
    },
    "depends": [
        "hr",
    ],
    "data": [
        "views/hr_department.xml",
    ],
}
