.. :changelog:

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

**Documentation**


9.4.1 (2016-11-11)
++++++++++++++++++

**Features and Improvements**

**Bugfixes**

**Build**

**Documentation**


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

