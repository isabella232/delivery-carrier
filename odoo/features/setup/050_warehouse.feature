# -*- coding: utf-8 -*-
@swisslux @setup @warehouse

Feature: Configure Warehouse and Logistic processes

  @traceability
  Scenario: Configure traceability
    Given I set "Lots and Serial Numbers" to "Track lots or serial numbers" in "Inventory" settings menu
    Given I enable "Barcode scanner support" in "Inventory" settings menu

  @accounting
  Scenario: Inventory valuation
    Given I set "Inventory Valuation" to "Periodic inventory valuation (recommended)" in "Inventory" settings menu

  @location
  Scenario: Location & Warehouse configuration
    Given I set "Multi Locations" to "Manage several locations per warehouse" in "Inventory" settings menu
    Given I set "Routes" to "Advanced routing of products using rules" in "Inventory" settings menu
    Given I set "Dropshipping" to "Allow suppliers to deliver directly to your customers" in "Inventory" settings menu

  @wh_config
  Scenario: Configure main warehouse
    Given I find a "stock.warehouse" with oid: stock.warehouse0
    And having:
      | key             | value         |
      | name            | Swisslux AG   |
      | reception_steps | three_steps   |
      | delivery_steps  | ship_only     |

  @transit_location
  Scenario: Configure dedicated transit location for supplier in China
    Given I need an "stock.location" with oid: scenario.location_transit_cn
    And having:
      | key             | value                                     |
      | name            | Swisslux AG: Departure from China         |
      | usage           | transit                                   |
      | location_id     | by oid: stock.stock_location_locations    |
      | active          | True                                      |
      | return_location | False                                     |
      | scrap_location  | False                                     |

  @picking_type
  Scenario: Configure dedicated picking type to receive goods from transit location
    Given I need an "stock.picking.type" with oid: scenario.picking_type_receive_cn
    And having:
      | key                         | value                                 |
      | name                        | Receive from China                    |
      | default_location_dest_id    | by oid: scenario.location_transit_cn  |
      | code                        | incoming                              |
      | sequence_id                 | by name: Swisslux AG Sequence in      |
      | warehouse_id                | by oid: stock.warehouse0              |
      | return_picking_type_id      | by oid: stock.picking_type_out        |

   @push_rules
   Scenario: Add a global push rule to receive goods from transit location
     Given I need an "stock.location.path" with oid: scenario.location_path_transit_to_slx
     And having:
      | key                 | value                                 |
      | name                | Receive from China                    |
      | active              | True                                  |
      | location_from_id    | by oid: scenario.location_transit_cn  |
      | location_dest_id    | by oid: stock.stock_location_company  |
      | auto                | manual                                |
      | picking_type_id     | by oid: stock.picking_type_in         |
      | delay               | 0                                     |
  
  @procurement_rule
  Scenario: Configure the propagation of procurement order on "buy" rule
    Given I find an "procurement.rule" with name: Swisslux AG:  Buy
    And having:
      | key                         | value     |
      | propagate                   | True      |
      | group_propagation_option    | propagate |

  @reception_text_company
  Scenario: set default company reception text
    Given I execute the SQL commands
    """;
    update res_company set receipt_checklist = '
    _____ Anleitung Deutsch
    _____ Anleitung Franz.
    _____ Anleitung Ital.
    _____ Verpackung
    _____ Lieferumfang
    _____ Funktionstest

    Charge: __________________________ 
    
    Technik:
    Produktenews: JA / NEIN
    Visum: ____________________________';
    """

  @csv @reception_text_article_default
  Scenario: import products for ir_values
    Given "ir.values" is imported from CSV "setup/ir_values.csv" using delimiter ","
  
  @occasion
  Scenario: Occasion management
    Given I need an "stock.location" with oid: scenario.location_occasion
    And having:
      | key             | value       |
      | name            | Vorrat      |
      | usage           | internal    |
      | location_id     | by name: WH |
      | active          | True        |
      | return_location | True        |
      | scrap_location  | False       |
  
  @occasion
  Scenario: Configure dedicated picking type from occasion
    Given I need an "stock.picking.type" with oid: scenario.picking_type_occasion
    And having:
      | key                      | value                                  |
      | name                     | Vorrat Sendung                         |
      | default_location_dest_id | by oid: stock.stock_location_customers |
      | default_location_src_id  | by oid: scenario.location_occasion     |
      | code                     | outgoing                               |
      | use_existing_lots        | True                                   |
      | active                   | True                                   |
      | sequence_id              | by name: Swisslux AG Sequence in       |
      | warehouse_id             | by oid: stock.warehouse0               |
      | return_picking_type_id   | by oid: stock.picking_type_out         |
  
  @occasion
  Scenario: Configure dedicated picking type from occasion
    Given I need an "stock.location.route" with oid: scenario.location_route
    And having:
      | key                      | value                       |
      | name                     | Swisslux AG: Vorrat Sendung |
      | product_selectable       | True                        |
      | sale_selectable          | True                        |
      | product_categ_selectable | True                        |
      | warehouse_selectable     | True                        |
      | active                   | True                        |
      | sequence                 | 10                          |
      | warehouse_ids            | by oid: stock.warehouse0    |
  
  @occasion
  Scenario: Configure the propagation of procurement order for occasion
    Given I need an "procurement.rule" with oid: scenario.procurement_rule_occasion
    And having:
      | key             | value                                  |
      | action          | move                                   |
      | active          | True                                   |
      | procure_method  | make_to_stock                          |
      | name            | WH: Vorrat -> Customers                |
      | delay           | 0                                      |
      | picking_type_id | by oid: scenario.picking_type_occasion |
      | location_id     | by oid: stock.stock_location_customers |
      | route_sequence  | 10                                     |
      | sequence        | 20                                     |
      | warehouse_id    | by oid: stock.warehouse0               |
      | route_id        | by oid: scenario.location_route        |
      | location_src_id | by oid: scenario.location_occasion     |
      | propagate       | True                                   |
    
  @occasion
  Scenario: Configure the route occasion to have the correct pull
    Given I find an "stock.location.route" with oid: scenario.location_route
    And having:
      | key      | value                                      |
      | pull_ids | by oid: scenario.procurement_rule_occasion |
     
  @retour
  Scenario: Retour management
    Given I need an "stock.location" with oid: scenario.location_retour_in
    And having:
      | key             | value       			|
      | name            | Retouren (Eingang) 	|
      | usage           | internal    			|
      | location_id     | by name: WH 			|
      | active          | True        			|
      | return_location | True        			|
      | scrap_location  | False       			|
    Given I need an "stock.location" with oid: scenario.location_retour_qc
    And having:
      | key             | value       			|
      | name            | Retouren (Qualität) 	|
      | usage           | internal    			|
      | location_id     | by name: WH 			|
      | active          | True        			|
      | return_location | True        			|
      | scrap_location  | False       			|
      
  @retour
  Scenario: Configure dedicated picking type for retour
    Given I need an "stock.picking.type" with oid: scenario.picking_type_retour
    And having:
      | key                      | value                                  |
      | name                     | Retouren (receipt)                     |
      | default_location_dest_id | by oid: scenario.location_retour_in    |
      | default_location_src_id  | by oid: stock.stock_location_customers |
      | code                     | incoming                               |
      | use_existing_lots        | True                                   |
      | active                   | True                                   |
      | sequence_id              | by name: Swisslux AG Sequence in       |
      | warehouse_id             | by oid: stock.warehouse0               |
    Given I need an "stock.picking.type" with oid: scenario.picking_type_retour_int
    And having:
      | key                      | value                                  |
      | name                     | Retouren (internal transfer)           |
      | default_location_dest_id | by oid: scenario.location_retour_qc    |
      | default_location_src_id  | by oid: scenario.location_retour_qc    |
      | code                     | internal                               |
      | use_existing_lots        | True                                   |
      | active                   | True                                   |
      | sequence_id              | by name: Swisslux AG Sequence in       |
      | warehouse_id             | by oid: stock.warehouse0               |
      
  @retour
  Scenario: Configure dedicated route for retour
    Given I need an "stock.location.route" with oid: scenario.location_route_retour
    And having:
      | key                      | value                       			|
      | name                     | Swisslux AG: Retouren für Kontrolle	|
      | product_selectable       | True                        			|
      | sale_selectable          | True                        			|
      | product_categ_selectable | True                        			|
      | warehouse_selectable     | True                        			|
      | active                   | True                        			|
      | sequence                 | 10                          			|
      | warehouse_ids            | by oid: stock.warehouse0    			|
      
  @retour
  Scenario: Configure dedicated path for retour
  	Given I need an "stock.location.path" with oid: scenario.location_path_retour
  	And having:
  	  | key                      | value                       					|
  	  | active					 | True								 			|
  	  | auto				     | manual										|
  	  | location_from_id		 | by oid: scenario.location_retour_in			|  	  
  	  |	location_dest_id         | by oid: scenario.location_retour_qc		    |
  	  |	name					 | WH: Retour Input -> Retour Quality Control	|
  	  |	picking_type_id  	     | by oid: scenario.picking_type_retour_int		|
  	  |	propagate				 | True											|
  	  |	route_id				 | by oid: scenario.location_route_retour		|
  	  
  @retour
  Scenario: Update dedicated route for retour
    Given I find an "stock.location.route" with oid: scenario.location_route_retour
    And having:
      | key                      | value                       				|
  	  | push_ids				 | by oid: scenario.location_path_retour	|
  	  

