# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from pkg_resources import Requirement, resource_stream
from anthem.lyrics.loaders import load_csv_stream

req = Requirement.parse('swisslux-odoo')


def load_csv(ctx, path, model, delimiter=',',
             header=None, header_exclude=None):
    content = resource_stream(req, path)
    load_csv_stream(ctx, model, content, delimiter=delimiter,
                    header=header, header_exclude=header_exclude)


def load_csv_no_tracking(ctx, path, model, delimiter=',',
                         header=None, header_exclude=None):
    if isinstance(model, str):
        model = ctx.env[model]
    model = model.with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, path, model, delimiter, header, header_exclude)
