# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "CSV Exports",
    "summary": "CSV exports to sftp for PRIME",
    "version": "11.0.1.0.0",
    "category": "Swisslux Modules",
    "website": "https://odoo-community.org/",
    "author": "Camptocamp",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "views/csv_export.xml",
        "data/ir_cron.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
    ],
}
