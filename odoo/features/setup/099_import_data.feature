# -*- coding: utf-8 -*-
@swisslux @setup @import

Feature: import master data

  @csv @regions
  Scenario: import specific regions
    Given "res.partner.region" is imported from CSV "setup/res.partner.region.csv" using delimiter ","

  @csv @zip
  Scenario: update zip with linked regions
    Given "res.better.zip" is imported from CSV "setup/res.better.zip.csv" using delimiter ","

  @csv @product_categories
  Scenario: import product categories
    Given "product.category" is imported from CSV "setup/product.category.csv" using delimiter ","

  @csv @product_expenses
  Scenario: import products for expenses
    Given "product.product" is imported from CSV "setup/product_expenses.csv" using delimiter ","
  
  @csv @service_categories
  Scenario: import service categories
    Given "product.category" is imported from CSV "setup/service-artikel-kategorien.csv" using delimiter ","
    
  @csv @service_article
  Scenario: import service articles
    Given "product.product" is imported from CSV "setup/service-artikel.csv" using delimiter ","
  
  @csv @product_informations
  Scenario: setup new fields for product
    Given "product.class" is imported from CSV "setup/product.class.csv" using delimiter ","
    Given "product.color.code" is imported from CSV "setup/product.colorcode.csv" using delimiter ","
    Given "product.harmsys.code" is imported from CSV "setup/product.harmsyscode.csv" using delimiter ","
    Given "product.manual.code" is imported from CSV "setup/product.manualcode.csv" using delimiter ","
    
  @csv @products @slow
  Scenario: import products
    Given "product.product" is imported from CSV "setup/product.product.csv" using delimiter ","
    
  @csv @products_trad @slow
  Scenario: import products
    Given I set the context to "{'lang':'en_US'}"
      And "product.product" is imported from CSV "setup/product_en.csv" using delimiter ","
    Given I set the context to "{'lang':'fr_FR'}"
      And "product.product" is imported from CSV "setup/product_fr.csv" using delimiter ","
    Given I set the context to "{'lang':'it_IT'}"
      And "product.product" is imported from CSV "setup/product_it.csv" using delimiter ","

  @update_reception_text_product @product
  Scenario: set default product reception text
    Given I execute the SQL commands
    """;
    update product_template set receipt_checklist = '
    Technik (DRINGEND):
    Lieferumfang Logistik:

    Label aussen

    Label innen

    Anleitungen D+F

    Merkblatt V5.0';
    """

  @partner_title
  Scenario: add Department title
    Given I need a "res.partner.title" with oid: scenario.partner_title_department
      And having:
        | key  | value     |
        | name | Department |

  @csv @pricelists
  Scenario: import specific pricelist
    Given "product.pricelist" is imported from CSV "setup/product.pricelist.csv" using delimiter ","

  @csv @pricelist_items @slow
  Scenario: import specific pricelist items
    Given "product.pricelist.item" is imported from CSV "setup/product.pricelist.item.csv" using delimiter ","

  @csv @orderpoint @slow
  Scenario: import specific orderpoint
    Given "stock.warehouse.orderpoint" is imported from CSV "setup/stock.warehouse.orderpoint.csv" using delimiter ","
    
    @csv @orderpoint_minmax @slow
  Scenario: import specific orderpoint
    Given "stock.warehouse.orderpoint" is imported from CSV "setup/stock.warehouse.orderpoint_min_max.csv" using delimiter ","

  @csv @bom @slow
  Scenario: import specific bom
    Given "mrp.bom" is imported from CSV "setup/mrp.bom.csv" using delimiter ","
    
  @csv @projects
  Scenario: import specific projects
    Given "project.project" is imported from CSV "setup/project.csv" using delimiter ","
    
  @csv @partner_category
  Scenario: import partner categories
    Given "res.partner.category" is imported from CSV "setup/res.partner.category.csv" using delimiter ","
    
  @csv @partner @slow
  Scenario: import partner
    Given "res.partner" is imported from CSV "setup/res.partner.csv" using delimiter ","

  @csv @partner_contacts @slow
  Scenario: import specific partner contacts
    Given "res.partner" is imported from CSV "setup/res.partner_contacts.csv" using delimiter ","

  @csv @supplierinfo @slow
  Scenario: import specific supplierinfo
    Given "product.supplierinfo" is imported from CSV "setup/product.supplierinfo.csv" using delimiter ","

