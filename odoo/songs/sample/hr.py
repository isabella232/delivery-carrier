# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from ..common import load_csv, load_csv_no_tracking


@anthem.log
def update_admin_user(ctx):
    ctx.env.ref('base.user_root').write({
       'tz': 'Europe/Zurich',
    })


@anthem.log
def delete_default_departments(ctx):
    ctx.env['hr.department'].search([
        ('name', 'in', ['Administration', 'Sales']),
    ]).unlink()


@anthem.log
def import_departments(ctx):
    load_csv_no_tracking(ctx, 'data/sample/hr_department.csv', 'hr.department')


@anthem.log
def import_groups(ctx):
    # Group "project.group_tasks_work_on_tasks" no longer exists
    # in module project => removed from CSV
    load_csv_no_tracking(ctx, 'data/sample/res_groups.csv', 'res.groups')


@anthem.log
def import_users(ctx):
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/sample/res_users.csv', model)


@anthem.log
def import_employee_addresses(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/hr_employee_home_address.csv', 'res.partner')


@anthem.log
def import_employees(ctx):
    load_csv_no_tracking(ctx, 'data/sample/hr_employee.csv', 'hr.employee')


@anthem.log
def import_department_managers(ctx):
    load_csv_no_tracking(
        ctx, 'data/sample/hr_department_mgr.csv', 'hr.department')


@anthem.log
def setup_timesheet_activities(ctx):
    # FIXME specific_timesheet_activities is not migrated to V11 yet
    load_csv_no_tracking(
        ctx, 'data/sample/hr_timesheet_activity.csv',
        'hr.timesheet.sheet.activity')


@anthem.log
def main(ctx):
    """ Configuring HR """
    update_admin_user(ctx)
    delete_default_departments(ctx)
    import_departments(ctx)
    import_groups(ctx)
    import_users(ctx)
    import_employee_addresses(ctx)
    import_employees(ctx)
    import_department_managers(ctx)
    # setup_timesheet_activities(ctx)
