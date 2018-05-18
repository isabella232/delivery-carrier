.. :changelog:

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

* BSSLX-58: Create v11 base branch
* BSSLX-5: swisslux_sale module to V11
* BSSLX-7: Migrate swisslux_purchase to V11
* BSSLX-8: Migrate swisslux_mrp to V11
* BSSLX-9: Migrate swisslux_account to V11
* BSSLX-12: Migrate the module OCA stock_split_picking to V11
* BSSLX-13: swisslux_product module to V11
* BSSLX-19: Migrate swisslux_invoice to V11
* BSSLX-25: swisslux_translations module to V11
* BSSLX-37: swisslux_hr module to V11
* BSSLX-50: Migrate swisslux_stock to V11
* BSSLX-56: add OCA/project_department
* Upgrade nginx version to 11.0-1.2.2
* Upgrade dockerimage to 2.6.1
* BSSLX-53: incorporate PR with product_dimension module
* BSSLX-63: Fix minion build
* BSSLX-64: Fix the build with migrated database
* BSSLX-41/45: Install account_reconcile_rule_early_payment_discount
* BSSLX-6: Add stock_available_mrp
* BSSLX-46: add analytic_department
* Set MARABUNTA_MODE to migration mode
* BSSLX-18: Migrate swisslux_partner to V11
* BSSLX-62: Fix/update pending merges for V11
* BSSLX-3: Migrate specific_building_project to V11
* BSSLX-16: Migrate specific_company_group to V11
* BSSLX-67: Fix migration of module l10n_ch_pain_base

**Documentation**


9.10.0 (2018-03-06)
+++++++++++++++++++

**Features and Improvements**

* Update project-template with lastest updates

**Bugfixes**

* BIZ-1133: Error message opening VAT-report
* BIZ-992: Delivery slips are suddently bad again
* BIZ-705: Fix customer followup report CSS

**Build**

* Update with dockerimage 9.0-2.4.1


9.9.5 (2018-03-06)
++++++++++++++++++

**Bugfixes**

* BIZ-1394: Update production outgoing email settings


9.9.4 (2018-02-27)
++++++++++++++++++

**Bugfixes**

* BIZ-1412 Remove readonly on project_discount field from sale order line model
* BIZ-1093: Update odoo-cloud-platform


9.9.3 (2018-02-22)
++++++++++++++++++

**Bugfixes**

* BIZ-1394: URGENT: Change Email settings


9.9.2 (2018-02-07)
++++++++++++++++++

** Moved to 9.10.0

9.9.1 (2018-01-04)
++++++++++++++++++

**Features and Improvements**

* BIZ-1024: update products with new VAT


9.9.0 (2017-12-20)
++++++++++++++++++

**Features and Improvements**

* BIZ-1024:

  * Install module account_fiscal_position_rule
  * Install module account_fiscal_position_rule_purchase
  * Install module account_fiscal_position_rule_sale
  * Create fiscal position and rule for swiss VAT 2018


9.8.0 (2017-12-12)
++++++++++++++++++

**Bugfixes**

* BIZ-978 CSV-Export has stopped


9.7.5 (2017-11-20)
++++++++++++++++++

**Bugfixes**

* BIZ-705 Improve followup report layer


9.7.4 (2017-10-26)
++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* Update manufacture to fix dismantling issue BIZ-704

**Build**

**Documentation**


9.7.3 (2017-10-20)
++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* Fix category mapping in csv export of partner BIZ-644

**Build**

**Documentation**


9.7.2 (2017-10-09)
++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* Fix some reports layout problems in specific_reports
* Fix faulty cursor usage in customer csv export

**Build**

**Documentation**


9.7.1 (2017-10-03)
++++++++++++++++++

**Features and Improvements**

* Add SLX_TEST outgoing mail settings

**Bugfixes**

**Build**

**Documentation**


9.7.0 (2017-09-26)
++++++++++++++++++

**Features and Improvements**

* Add web_environment_ribbon

**Bugfixes**

**Build**

* Update docker-odoo-project from 9.0-2.2.0 -> 9.0-2.4.0
* Update with latest from odoo-template

**Documentation**


9.6.1 (2017-08-28)
++++++++++++++++++

**Features and Improvements**

**Bugfixes**

* Alignement in followup report

**Build**

**Documentation**

9.6.0 (2017-07-14)
++++++++++++++++++

**Features and Improvements**
* Customisation of Followup Report issue #4132 (https://odoo.priv.camptocamp.com/#id=4132&view_type=form&model=project.issue&menu_id=677&action=1014)
* Add new smtp server in integration

**Bugfixes**

**Build**

**Documentation**

9.5.8 (2017-05-15)
++++++++++++++++++

**Features and Improvements**
* Picking report : add PO name + use operations if present
* Propagate sale invoice on invoice
* Get the partner bank account when expense imported in payment order
* Allow to close a proforma invoice
* Allow to search on the supplier code product
* Add on change on specific price list in SO. see incident 4037

9.5.7 (2017-05-15)
++++++++++++++++++

**Features and Improvements**
* Fix missing template in purchase Order


9.5.5 (2017-04-24)
++++++++++++++++++

**Features and Improvements**
* Fix exporting CSV, no file generated if data is empty
* Remove not more used field in partner export
* Add page count on inventory report

9.5.4 (2017-02-13)
++++++++++++++++++

**Features and Improvements**
* Fix payment order maturity date
* Fix invoice report turnover
* Fix export csv delimiter for partner and contact
* Add partner title translated in export csv

9.5.3 (2017-02-13)
++++++++++++++++++

**Features and Improvements**
* Add S3 management for Shipping Label


9.5.2 (2017-02-09)
++++++++++++++++++

**Features and Improvements**
* Add procurement group on MO and propagated on stock move
* Cancelling a MO, cancel all related move
* The PO procurement group is propagated, on all related stock move (event on buy from china route)
* Fix CSV exporting contact, remove 'False' inside fields, add escape caracter on text fields
* Improve Report picking Layout
* Improve of display partner (Name, City (Ref))
* Add script to recompute display parter
* Add module to report on Company Group (Turnover Report)
* Add check to prevent to cancelling a move if the parent is not cancelled


9.5.1 (2016-01-05)
++++++++++++++++++

**Features and Improvements**

* Script post install to ignore the partners created/modified before 16-12-01
* Set CRON unactive at installation

**Bugfixes**

* Fix csv if there is no "influence"


**Build**

**Documentation**


9.5.0 (2016-12-21)
++++++++++++++++++

**Features and Improvements**

* Add module for exporting partners in csv to sftp server
* Add configuration for SFTP in server env configuration files


**Bugfixes**

**Build**

**Documentation**


9.4.12 (2016-12-21)
+++++++++++++++++++

**Bugfixes**
* Allow multiple same supplier reference on supplier invoice

9.4.11 (2016-12-16)
+++++++++++++++++++

**Features and Improvements**
* New logs for Redis
**Bugfixes**
* inactivate security rules for building project
* reset a new sequence on dupplicate products


9.4.10 (2016-12-08)
+++++++++++++++++++

**Bugfixes**
* Linked opportunity to quotation even if it's a building project
* If partner is a contact, it will take the company to get the related pricelist
* customer reference with comma is replaced by / also on creation


9.4.9 (2016-11-30)
++++++++++++++++++

**Features and Improvements**
* Add configuration for email
* Add Chat configuration
**Bugfixes**
* Fix reference on invoice, the customer ref comma are replace by a '/' on sale order when saved
* Building project : Business provider blank when create a quotation from an opportunity + Prevent dupplicate pricelist if partner equal to business provider
* E-nr add on shipping report + split it in bloc of 3 character at printing
* Remove size limit on delivery slip report, now the customer reference is printed on the full page size
* Add support for ZKB
* Fix sale order address delivery


9.4.8 (2016-11-22)
++++++++++++++++++

**Features and Improvements**
* Add new rule for china
**Bugfixes**
* Remove contraints for unique account number for partner bank
* Remove required for ref on partner form
* Change Order print layout of date
* Change Invoice print layout
* Fix invoice xmlid reference for partner_90424


9.4.7 (2016-11-18)
++++++++++++++++++

**Bugfixes**
* Fix company instead of contact in building project
* Fix new CSV file (imported in production)
* Scenario to rename Stock Order point + fix sequence next val
* Set ref on partner is missing + fix sequence next val
* Cancel WH/OUT/00019
* Remove All OP from Stock with OP as name


9.4.6 (2016-11-15)
++++++++++++++++++

**Features and Improvements**
* When you deactivate a company it deactivate related contact
**Bugfixes**
* Fix layout overlay in delivery slip
* Fix invoice additionnal comma if company is selected instead of contact
* Fix translation in quotation report


9.4.5 (2016-11-14)
++++++++++++++++++

**Bugfixes**
* Fix typo in xml id for payment term in invoice report

9.4.4 (2016-11-14)
++++++++++++++++++

**Bugfixes**

* When an attachment is deleted and is stored on a different Object Storage
  bucket than the current one, do not delete it from the bucket

**Build**

* Start integration on only 1 host
* Start integration with 2 workers


9.4.3 (2016-11-11)
++++++++++++++++++

**Features and Improvements**
* Improve CSV data files
**Bugfixes**
* Change sequence on pricelist, user can order item per sequence
* Change layout test work_email on sale order report


9.4.2 (2016-11-11)
++++++++++++++++++

**Build**

* Rename databases with _ instead of -


9.4.1 (2016-11-11)
++++++++++++++++++

**Build**

* Rename databases on the Rancher instances with anonymous names


9.4.0 (2016-11-08)
++++++++++++++++++

**Features and Improvements**
* Logs output as Json
* Metrics sent as UDP to statsd(Grafana)


9.3.7 (2016-11-08)
++++++++++++++++++

**Bugfixes**
* Fix working_email in report header
* Get right delivery adress and invoicing address on sale order

9.3.6 (2016-11-04)
++++++++++++++++++

**Bugfixes**

* Fix customer/supplier field on contact if parent company is customer/supplier
* Add security for specific_invoice

9.3.5 (2016-10-31)
++++++++++++++++++

**Bugfixes**

* Cloud Platform: rework of ``attachment_s3`` which makes
  ``AWS_ATTACHMENT_READONLY`` useless and correct a bug that deletes existing
  attachments (mainly assets)


9.3.4 (2016-10-30)
++++++++++++++++++

**Data**

* Import 'slow' data

* Fixes in contacts:
  * replaced in 'influence':
    * I_A by installer_a
    * I_B by installer_b
    * I_C by installer_c
    * P_A by planer_A
    * P_B by planer_B
    * P_C by planer_C
    * G_A by wholesale_a
    * G_B by wholesale_b
    * G_C by wholesale_c
    * Z by key_contact
  * emptied field 'property_stock_location' wrongly set to ' Land.Caption_Caption09' on every record
  * moved invalid contacts (columns shifted) in 'invalid_contacts.csv'
  * added missing partner titles Project Manager and Ms
* in partner headquarter: removed lines without any link (faster import)


9.3.3 (2016-10-29)
++++++++++++++++++

**Data**

* add a missing partner used by supplier infos
* remove slow imports from the release, will be imported in the next release


9.3.2 (2016-10-28)
++++++++++++++++++

**Data**

* Removed invalid partners (and their contacts) from the data files


9.3.1 (2016-10-28)
++++++++++++++++++

**Features and Improvements**

* Update data setup files


9.3.0 (2016-10-27)
++++++++++++++++++

**Features and Improvements**

* Add scenario for occasion locations
* Add final data files

**Bugfixes**

* Fix order position
* Fix translations
* account invoice: public_discount can be filled manually
* Fix layout of reports
* add report inventory email layout
* fix carrier_type field name in postlogistic

**Build**

* Configure composition files for production
* Add the cloud platform addons and configuration


9.2.0 (2016-10-20)
++++++++++++++++++

**Features and Improvements**
* Add field number_shipments in view & reports & translations
* Add E_nr in the internal_picking report
* Add VAT on Quotations/SO in the so_lines

**Bugfixes**
* Use display_name in building_project kanban view
* Delivery document with name of the SO customer on it
* Add Invoice document: Add more spaces inbetween the address and the title of the document
* Pricelist import: don't create default item
* Fix default_code in delivery slip

**Build**

**Documentation**


9.1.0 (2016-09-29)
++++++++++++++++++

First docker release!
