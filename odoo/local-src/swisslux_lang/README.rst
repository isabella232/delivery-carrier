==========================
Swisslux language settings
==========================

The purpose of this module is to keep custom language configuration intact after
upgrading `base` module.

`res.lang` records defined there are stored as CSV file, and therefore those
records are updated at every `base` upgrade, which leads to loss of all
customisations, including those made by songs. Having such module means that
languages of our interest are updated once more.

NOTE
----
This module is a temporary workaround, at the moment of writing ticket to Odoo
core support is being prepared to solve the issue on a persistent basis.
