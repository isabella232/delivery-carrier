# -*- coding: utf-8 -*-
@swisslux @setup @hr

Feature: configure users, departments and employees

  ############################################################################
  # As the employee is attached to a department, and the department manager
  # is an employee, I have to import datas in the following sequence:
  # - import just department name, and hierarchy if any
  # - import employee
  # - import updated department list (with manager information)
  ############################################################################
  
  @admin_user
  Scenario: set admin user correctly
    Given I find a "res.users" with oid: base.user_root
    And having:
      | key         | value         |
      | tz          | Europe/Zurich |
  
  @department
  Scenario: delete default department
    Given I find a "hr.department" with name: Administration
    And I delete it
    Given I find a "hr.department" with name: Sales
    And I delete it
  
  @csv @static @department
  Scenario: import departments
    Given "hr.department" is imported from CSV "setup/hr_department.csv" using delimiter ","
    
  @csv @static @groups
  Scenario: import groups
    Given "res.groups" is imported from CSV "setup/res_groups.csv" using delimiter ","
  
  @csv @static @users  
  Scenario: import users
    Given "res.users" is imported from CSV "setup/res.users.csv" using delimiter ","

  @csv @static @employee_address
  Scenario: import personal address for employees
    Given "res.partner" is imported from CSV "setup/hr_employee_home_address.csv" using delimiter ","
    
  @csv @static @employee  
  Scenario: import employees
    Given "hr.employee" is imported from CSV "setup/hr.employee.csv" using delimiter ","

  @csv @static @dpt_mgr
  Scenario: import departments manager
    Given "hr.department" is imported from CSV "setup/hr_department_mgr.csv" using delimiter ","  

  @csv @static @ts_activity
  Scenario: setup timesheet activities
    Given "hr.timesheet.sheet.activity" is imported from CSV "setup/hr_timesheet_activity.csv" using delimiter ","

