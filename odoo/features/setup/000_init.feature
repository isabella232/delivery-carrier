# -*- coding: utf-8 -*-
@swisslux @setup

Feature: Parameter the new database
  In order to have a coherent installation
  I've automated the manual steps.

  @createdb @no_login
  Scenario: CREATE DATABASE
    Given I find or create database from config file

  @no_demo_data
  Scenario: deactivate demo data
    Given I update the module list
    And I do not want all demo data to be loaded on install

  @lang
  Scenario: install lang
   Given I install the following language :
      | lang    |
      | de_DE   |
      | fr_FR   |
      | it_IT   |
    Then the language should be available
    Given I find a "res.lang" with code: en_US
    And having:
      | key             | value     |
      | grouping        | [3,0]     |
      | iso_code        | en        |
      | date_format     | %m/%d/%Y  |
      | thousands_sep   | ,         |
      | decimal_point   | .         |
    Given I find a "res.lang" with code: de_DE
    And having:
      | key             | value     |
      | grouping        | [3,0]     |
      | date_format     | %d.%m.%Y  |
      | thousands_sep   | '         |
      | decimal_point   | .         |
    Given I find a "res.lang" with code: fr_FR
    And having:
      | key             | value     |
      | grouping        | [3,0]     |
      | date_format     | %d.%m.%Y  |
      | thousands_sep   | '         |
      | decimal_point   | .         |
    Given I find a "res.lang" with code: it_IT
    And having:
      | key             | value     |
      | grouping        | [3,0]     |
      | date_format     | %d.%m.%Y  |
      | thousands_sep   | '         |
      | decimal_point   | .         |

  @company
  Scenario: Configure main partner and company
  Given I find a "res.company" with oid: base.main_company
    And having:
       | key                | value                 |
       | name               | Swisslux AG           |
       | street             | Industriestrasse 8    |
       | street2            |                       |
       | zip                | 8618                  |
       | city               | Oetwil am See         |
       | country_id         | by code: CH           |
       | phone              | +41 43 844 80 80      |
       | fax                | +41 43 844 80 81      |
       | email              | info@swisslux.ch      |
       | website            | www.swisslux.ch       |
       | vat                | CHE-107.897.036 MWST  |
       | company_registry   | CHE-107.897.036       |
       | rml_header1        |                       |
    Given the company has the "images/company_logo.png" logo

    Given I need a "res.partner" with oid: base.main_partner
    And having:
       | key        | value                     |
       | name       | Swisslux AG               |
       | street     | Industriestrasse 8        |
       | street2    |                           |
       | zip        | 8618                      |
       | city       | Oetwil am See             |
       | country_id | by code: CH               |
       | phone      | +41 43 844 80 80          |
       | fax        | +41 43 844 80 81          |
       | email      | info@swisslux.ch          |
       | website    | www.swisslux.ch           |
       | lang       | de_DE                     |
       | company_id | by oid: base.main_company |
    Given I need a "res.partner" with oid: scenario.partner_swisslux_romandie
    And having:
       | key        | value                         |
       | name       | Swisslux SA                   |
       | street     | Chemin de la Grand Clos 17    |
       | street2    |                               |
       | zip        | 1092                          |
       | city       | Belmont-sur-Lausanne          |
       | country_id | by code: CH                   |
       | phone      | +41 21 711 23 40              |
       | fax        | +41 21 711 23 41              |
       | email      | info@swisslux.ch              |
       | website    | www.swisslux.ch               |
       | type       | other                         |
       | lang       | fr_FR                         |
       | parent_id  | by oid: base.main_partner     |
       | company_id | by oid: base.main_company     |
    And the partner has the "images/company_logo.png" image

  @force_translations
  Scenario: Force lang translations
    Given I update the module list
    When I update the following languages
         | lang  |
         | de_DE |

  @logo
  Scenario: setup specific logo for company reports
    Given I find a "res.company" with oid: base.main_company
    And the company has the "images/company_logo_header.png" report logo

  @url
  Scenario: setup url
    Given I update web.base.url with full url "http://localhost:8069"
    Then I freeze web.base.url

  @address
  Scenario: set good address format
    Given I execute the SQL commands
    """;
    update res_country set address_format = '%(street)s
    %(street2)s
    %(country_code)s-%(zip)s %(city)s' where code like 'CH';
    """

  @decimal_precision
  Scenario: adjust decimal precision for product uom
    Given I need an "decimal.precision" with oid: product.decimal_product_uom
    And having:
      | key     | value |
      | digits  | 1     |

  @version
  Scenario: setup application version
    Given I set the version of the instance to "1.0.0"    
