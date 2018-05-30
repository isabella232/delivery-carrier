# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from anthem.lyrics.records import create_or_update
from ..common import load_csv


@anthem.log
def archive_default_data(ctx):
    create_or_update(ctx, 'project.project', 'project.project_project_data', {
        'active': False,
    })


@anthem.log
def configure_project(ctx):
    # set "Time on Tasks" to "Manage time estimation on tasks"
    # FIXME missing config?
    pass


@anthem.log
def delete_task_stages(ctx):
    ctx.env['ir.translation'].search([
        ('name', '=', 'project.task.type,name'),
    ]).unlink()
    ctx.env['ir.model.data'].search([
        ('model', '=', 'project.task.type'),
    ]).unlink()
    ctx.env['project.task.type'].search([]).unlink()


@anthem.log
def configure_task_stages(ctx):
    records = [
        {'xmlid': '__setup__.stage_01',
         'name': 'New',
         'sequence': 1,
         'fold': False,
         'closed': False,
         'case_default': True,
         },
        {'xmlid': '__setup__.stage_02',
         'name': 'In Progress',
         'sequence': 2,
         'fold': False,
         'closed': False,
         'case_default': True,
         },
        {'xmlid': '__setup__.stage_03',
         'name': 'Postponed',
         'sequence': 3,
         'fold': False,
         'closed': False,
         'case_default': True,
         },
        {'xmlid': '__setup__.stage_04',
         'name': 'Completed',
         'sequence': 4,
         'fold': False,
         'closed': False,
         'case_default': True,
         },
    ]
    for record in records:
        xmlid = record.pop('xmlid')
        create_or_update(ctx, 'project.task.type', xmlid, record)

    for lang in ['de_DE', 'fr_FR', 'it_IT']:
        model = ctx.env['project.task.type'].with_context({
            'tracking_disable': True,
            'lang': lang,
        })
        load_csv(
            ctx, 'data/sample/project_task_stages_%s.csv' % lang[:2], model)


@anthem.log
def create_building_project_template(ctx):
    create_or_update(
        ctx, 'project.project', '__setup__.project_building_template', {
            'name': 'Template for building project',
            'building_template': True,
        })


@anthem.log
def main(ctx):
    """ Configuring projects """
    archive_default_data(ctx)
    configure_project(ctx)
    delete_task_stages(ctx)
    configure_task_stages(ctx)
    create_building_project_template(ctx)
