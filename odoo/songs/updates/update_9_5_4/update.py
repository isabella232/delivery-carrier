# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from pkg_resources import resource_stream, Requirement

import anthem
from anthem.lyrics.loaders import load_csv_stream

@anthem.log
def import_group_data(ctx, req):
    """ Importing product template """
    content = resource_stream(
        req, 'data/upgrade_9_5_4/res.groups_slx_confidential.csv')
    load_csv_stream(ctx, 'res.groups', content, delimiter=',')



@anthem.log
def main(ctx):
    """ Loading data """
    req = Requirement.parse('swisslux-odoo')
    import_group_data(ctx, req)
