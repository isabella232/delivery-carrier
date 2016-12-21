# -*- coding: utf-8 -*-
# Author: Denis Leemann
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
# from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from csv_export import CSVExporter
# from sftp_interface import SFTPInterface
# from openerp import exceptions
import paramiko

EXPORT_DATE_FORMAT = '%d/%m/%Y'

EXPORT_FIELDS_CONTACTS = [
    ('ref', 'AccountContact_InterfaceKey1', None),
    ('active', 'AccountContact_Active', 'boolean_number'),
    ('get_parent_id_ref', 'AccountContact_Account_ID', None),
    ('title', 'AccountContact_Salutation', None),
    ('lastname', 'AccountContact_LastName', None),
    ('firstname', 'AccountContact_FirstName', None),
    ('phone', 'AccountContact_Phone1', None),
    ('mobile', 'AccountContact_Mobile1', None),
    ('fax', 'AccountContact_Fax1', None),
    ('lang', 'AccountContact_Language_Dimension_ID', None),
    ('email', 'AccountContact_Email1', None),
    ('function', 'AccountContact_Function', None),
    ('get_partner_state', 'AccountContact_Flag_Dimension_ID', None),
    ('get_influence', 'AccountContact_Influence_Dimension_ID', None),
    ('department', 'AccountContact_Department', None),
    ('comment', 'AccountContact_Remarks', None),
]

EXPORT_FIELDS_ADRESSES = [
    ('ref', 'Account_InterfaceKey1', None),
    ('active', 'Account_Active', 'boolean_number'),
    ('name', 'Account_LastName', None),
    ('street', 'Account_Street', None),
    ('zip', 'Account_PostalCode', None),
    ('city', 'Account_City', None),
    ('get_country_id_name', 'Account_Country_Dimension_ID', None),
    ('get_state_name', 'Account_State', None),
    ('get_user_id', 'Account_Sales_Personnel_ID', None),
    ('phone', 'Account_Phone1', None),
    ('fax', 'Account_Fax1', None),
    ('lang', 'Account_Language_Dimension_ID', None),
    ('website', 'Account_Website1', None),
    ('mobile', 'Account_Mobile1', None),
    ('email', 'Account_Email1', None),
]

EXPORT_FIELDS_TAGS = [
    ('ref', 'Account_InterfaceKey1', None),
    ('get_export_tags', 'ItemAdditionalRelation_Related_Item_ID', 'm2m'),
]

PADDING_ADRESSES_FIELDS = [
    ('Account_Sales', 1),
    ('Account_Purchase', 1),
    ('Account_Purchase_Taxcode_ID', 326),
    ('Account_Sales_Taxcode_ID', 301),
    ('Account3_Sales_Ertrag_ID', 6000),
    ('Account_Sales_FinancialAccount_ID', 1050),
    ('Account_Purchase_Currency_ID', 'CHF'),
    ('Account_Sales_Currency_ID', 'CHF'),
    ('Account3_Purchase_Ertrag_ID', 4690),
    ('Account_Purchase_FinancialAccount_ID', 4000),
    ('Account_Sales_PaymentCondition_ID', 1),
    ('Account_Purchase_PaymentCondition_ID', 1),
    ('Account_Sales_Shipping_Dimension_ID', 5)
]

EXPORT_TAGS = [
    ('scenario.partner_category_10', '008'),
    ('scenario.partner_category_11', '011'),
    ('scenario.partner_category_12', '009'),
    ('scenario.partner_category_13', '012'),
    ('scenario.partner_category_15', 'ABB'),
    ('scenario.partner_category_16', 'Alpiq'),
    ('scenario.partner_category_17', 'BK'),
    ('scenario.partner_category_18', 'BKW'),
    ('scenario.partner_category_19', 'BUR'),
    ('scenario.partner_category_2', '002'),
    ('scenario.partner_category_20', 'ELEKTROBAER'),
    ('scenario.partner_category_21', 'EKZ'),
    ('scenario.partner_category_22', 'EM'),
    ('scenario.partner_category_23', 'F&C'),
    ('scenario.partner_category_24', 'OF'),
    ('scenario.partner_category_25', 'SAESSELI'),
    ('scenario.partner_category_26', 'SCHIBLI'),
    ('scenario.partner_category_27', 'SONEPAR'),
    ('scenario.partner_category_28', 'WF'),
    ('scenario.partner_category_29', 'ZIEG'),
    ('scenario.partner_category_3', '001'),
    ('scenario.partner_category_30', 'KNXSwiss'),
    ('scenario.partner_category_31', '402'),
    ('scenario.partner_category_4', '004'),
    ('scenario.partner_category_5', '003'),
    ('scenario.partner_category_6', '005'),
    ('scenario.partner_category_7', '006'),
    ('scenario.partner_category_8', '007'),
    ('scenario.partner_category_9', '010'),
]


class ResPartner(models.Model):
    """
    Export CSV functionality
    """
    _inherit = "res.partner"

    contacts_last_xprt = fields.Datetime('Contacts Last Updated', store=True)
    adrs_tags_lst_xprt = fields.Datetime('Adresses Tags Last Updated')
    adrs_lst_xprt = fields.Datetime('Adresses Last Updated')

    @api.model
    def export_csv_contacts(self, domain=None, ftp=None, disk=None):
        """We want to export all the partners that are emmbedded into a company
        """
        exc = False

        self.env.cr.execute('SELECT id FROM res_partner '
                            'WHERE (parent_id IS NOT NULL) '
                            'AND (is_company IS False) '
                            'AND ((contacts_last_xprt is NULL) '
                            'OR (write_date> contacts_last_xprt) '
                            'OR (create_date> contacts_last_xprt))')
        ids = [row[0] for row in self.env.cr.fetchall()]
        partners = self.with_context(active_test=False).browse(ids)

        exporter = CSVExporter(partners, EXPORT_FIELDS_CONTACTS)
        exporter.generate_export()
        disk = '/tmp/partnercontact_'  # Set for dev purposes
        ftp = 'partnercontact_'
        if ftp is not None:
            try:
                exporter.save_to_sftp(ftp)
            except paramiko.SSHException as exc:
                pass
        elif disk is not None:
            exporter.save_to_disk(disk)

        if not exc:
            # Update the partners. Bypass the ORM in order not to modify the
            # write_date
            for partner in partners:
                self.env.cr.execute('UPDATE res_partner '
                                    'SET contacts_last_xprt=CURRENT_TIMESTAMP '
                                    'WHERE id = %s' % partner.id)
        file = exporter.get_data()
        res = {
            'exc': exc,
            'file': file,
            'ftp': ftp,
            'disk': disk,
        }
        return res

    @api.model
    def export_csv_partners(self):

        """ We want to export all the companies & the partners that have no
            companies
        """
        exc = False

        self.env.cr.execute("""SELECT id FROM res_partner
                            WHERE((((is_company is False)
                            AND (parent_id is Null))
                            OR (is_company is True))
                            AND ((adrs_lst_xprt is Null)
                            OR (write_date > adrs_lst_xprt)
                            OR (create_date > adrs_lst_xprt)))""")

        ids = [row[0] for row in self.env.cr.fetchall()]

        partners = self.with_context(active_test=False).browse(ids)

        exporter = CSVExporter(partners, EXPORT_FIELDS_ADRESSES,
                               PADDING_ADRESSES_FIELDS)
        exporter.generate_export()
        disk = '/tmp/partner_'  # TODO Set for dev purposes
        ftp = 'partner_'
        if ftp is not None:
            try:
                exporter.save_to_sftp(ftp)
            except paramiko.SSHException as exc:
                pass
        elif disk is not None:
            exporter.save_to_disk(disk)

        if not exc:
            # Update the partners. Bypass the ORM in order not to modify the
            # write_date
            for partner in partners:
                self.env.cr.execute('UPDATE res_partner '
                                    'SET adrs_lst_xprt=CURRENT_TIMESTAMP '
                                    'WHERE id = %s' % partner.id)
        file = exporter.get_data()
        res = {
            'exc': exc,
            'file': file,
            'ftp': ftp,
            'disk': disk,
        }
        return res

    @api.model
    def export_csv_partner_tags(self):
        """ We want to export all tags of partners with
            "company_type" = "company"
        """
        exc = False
        res = False

        sql = """SELECT id  FROM res_partner WHERE (is_company=True)
                 AND ((adrs_tags_lst_xprt is Null)
                 OR (write_date > adrs_tags_lst_xprt)
                 OR (create_date > adrs_tags_lst_xprt))"""

        self.env.cr.execute(sql)
        ids = [row[0] for row in self.env.cr.fetchall()]
        partners = self.with_context(active_test=False).browse(ids)
        exporter = CSVExporter(partners, EXPORT_FIELDS_TAGS, quote_all=False)
        exporter.generate_export()
        disk = '/tmp/Identifier_partnertags_'
        ftp = 'Identifier_partnertags_'
        if ftp is not None:
            try:
                exporter.save_to_sftp(ftp)
            except paramiko.SSHException as exc:
                pass
        elif disk is not None:
            exporter.save_to_disk(disk)

        if not exc:
            # Update the partners. Bypass the ORM in order not to modify the
            # write_date
            for partner in partners:
                self.env.cr.execute('UPDATE res_partner '
                                    'SET adrs_tags_lst_xprt=CURRENT_TIMESTAMP '
                                    'WHERE id = %s' % partner.id)
        file = exporter.get_data()
        res = {
            'exc': exc,
            'file': file,
            'ftp': ftp,
            'disk': disk,
        }
        return res

    @api.model
    def get_parent_id_ref(self):

        parent_ref = self.parent_id.ref

        return parent_ref

    @api.model
    def get_partner_state(self):
        if self.partner_state == 'qualified':
            return 'qualifiziert - Person'
        elif self.partner_state == 'potential_partner':
            return 'Kontaktpflege aktuell - Person'
        elif self.partner_state == 'active':
            return 'potentieller Partner - Person'

    @api.model
    def get_country_id_name(self):
        country_name = self.country_id.code
        if country_name == 'IT':
            return 'I'
        elif country_name == 'FR':
            return 'F'
        elif country_name == 'DE':
            return 'D'
        elif country_name == 'US':
            return 'USA'
        else:
            return country_name

    @api.model
    def get_state_name(self):
        if self.state_id.code:
            return self.state_id.code

    @api.model
    def get_user_id(self):
        if self.user_id.login:
            return self.user_id.login

    @api.model
    def get_export_tags(self):
        if self.category_id:
            values = ()
            for tag in self.category_id:
                for tag_ref in EXPORT_TAGS:
                    if self.env.ref(tag_ref[0]) == tag:
                        values = values + (tag_ref[1],)

            return values

    @api.model
    def get_influence(self):
        key = self.influence
        value = dict(self.fields_get(allfields=['influence'])
                     ['influence']['selection'])[key]
        if value == "Schluesselkontakt":
            value = "Schlüsselkontakt"
        return value
