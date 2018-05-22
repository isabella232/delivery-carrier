# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from io import StringIO

import os
import time
import unicodecsv as csv
import base64
import collections

import logging

import odoo.osv.orm as orm
from .sftp_interface import SFTPInterface

from odoo.addons.server_environment import serv_config
from odoo import api, fields, models

_logger = logging.getLogger()

SERV_CONFIG_SECTION = 'sftp_csv'


class CSVExporter(object):

    def __init__(self, records, export_mapping, export_padding=False,
                 encoding='utf-8', quote_all=True, quotechar='"',
                 separator=';', escapechar='\\'):
        model = records and records[0]._name or 'unknown model'
        _logger.info('export %d %s', len(records), model)
        self._records = records
        self._export_mapping = export_mapping
        self.output = StringIO()
        self._export_padding = export_padding or None
        quoting = csv.QUOTE_MINIMAL
        if quote_all:
            quoting = csv.QUOTE_ALL

        self.csv_writer = csv.writer(self.output,
                                     encoding=encoding,
                                     dialect='excel',
                                     doublequote=False,
                                     quotechar=quotechar,
                                     quoting=quoting,
                                     escapechar=escapechar,
                                     delimiter=separator)

    def generate_export(self):
        """ Export records according to mapping
        """
        self.write_headers()
        for record in self._records:
            row = []
            mapping = self._export_mapping
            written = False
            for odoo_field, external_field, type_field in mapping:
                try:
                    record = record.with_context(lang='de_DE')
                    value = record[odoo_field]
                    if isinstance(value, collections.Callable):
                        value = value()
                    if not value:
                        value = ''
                    if isinstance(value, orm.browse_record):
                        value = value.name_get()[0][1]
                    elif isinstance(value, orm.browse_record_list):
                        value = ','.join([x.name_get()[0][1] for x in value])
                    if (not value or value == '') and type_field:
                        if type_field == 'boolean':
                            value = 'False'
                        if type_field == 'number':
                            value = '0'
                        if type_field == 'NAfield':
                            value = 'n/a'
                    if value and type_field == 'CharLimit50':
                        value = value[:50]
                    if type_field == 'boolean_number':
                        value = '1' if value else '0'
                    if value and odoo_field == 'lang':
                        value = value[0].upper()
                    row.append(value)
                except KeyError:
                    if isinstance(getattr(record, odoo_field, None),
                                  collections.Callable):
                        if type_field == 'm2m':
                            values = getattr(record, odoo_field)()
                            if values and values != '':
                                for val in values:
                                    row.append(val)
                                    self.csv_writer.writerow(row)
                                    row.remove(val)
                            written = True
                        else:
                            value = getattr(record, odoo_field)()
                            row.append(value)
                    else:
                        # unknown field
                        _logger.warning('unknown field "%s"', odoo_field)
            if self._export_padding:
                for padding_name, padding_value in self._export_padding:
                    row.append(padding_value)
            if not written:
                self.csv_writer.writerow(row)

    def get_data(self):
        return self.output

    def write_headers(self):
        header = [x[1] for x in self._export_mapping]
        if self._export_padding:
            header += [x[0] for x in self._export_padding]
        self.csv_writer.writerow(header)

    def save_file(self, config_name_for_filename, additional_filename=None):
        sftp_or_disk = serv_config.get(SERV_CONFIG_SECTION, 'use_sftp_or_disk')
        filename = serv_config.get(SERV_CONFIG_SECTION,
                                   config_name_for_filename)
        if additional_filename:
            filename += additional_filename
        sftp = filename if sftp_or_disk == 'sftp' else None
        disk = filename if sftp_or_disk == 'disk' else None

        if sftp:
            self.save_to_sftp(sftp)
        elif disk:
            self.save_to_disk(disk)
        return self.output

    def save_to_disk(self, filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = filename + timestr + '.csv'
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, 'w') as out:
            out.write(self.output.getvalue())
            out.close()

    def save_to_sftp(self, filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename += timestr + '.csv'
        self.output.seek(0)
        sftp_interface = SFTPInterface()
        file = sftp_interface.save_output_to_sftp(self.output, filename)
        return (file, filename)


class CSVExporterFromList(CSVExporter):

    def __init__(self, records, export_mapping,
                 encoding='utf-8', quote_all=True, separator=';'):
        self._records = records
        self._export_mapping = export_mapping
        self.output = StringIO()

        quoting = csv.QUOTE_MINIMAL
        if quote_all:
            quoting = csv.QUOTE_ALL

        self.csv_writer = csv.writer(self.output,
                                     encoding=encoding,
                                     quoting=quoting,
                                     delimiter=separator)

    def generate_export_from_list(self):
        """ Export records according to mapping
        """
        self.write_headers()
        for record in self._records:
            row = []
            for value in record:
                row.append(value)

            self.csv_writer.writerow(row)


class CsvExportManager(models.Model):

    _name = 'csv.export.manager'
    _inherit = 'mail.thread'

    last_export = fields.Datetime(
        'Last Export',
        track_visibility=True
    )
    is_exported = fields.Boolean(
        string='Export Success',
        track_visibility=True
    )
    log = fields.Text(
        string='Log',
    )

    @api.model
    def export_contacts_partners(self):

        partner = self.env['res.partner']

        con = partner.export_csv_contacts()
        part = partner.export_csv_partners()
        tags = partner.export_csv_partner_tags()

        is_exported = not (con['exc'] or part['exc'] or tags['exc'])
        log = 'Contacts: ' + str(con['msg'] or '') + \
              ' | Partners: ' + str(part['msg'] or '') + \
              ' | Tags: ' + str(tags['msg'] or '')

        vals = {
            'last_export': fields.Datetime.now(),
            'is_exported': is_exported,
            'log': log,
        }
        export = self.create(vals)
        if con['file']:
            export.save_attachement('csv', con['file'], con['ftp'] or
                                    con['disk'])
        if part['file']:
            export.save_attachement('csv', part['file'], part['ftp'] or
                                    part['disk'])
        if tags['file']:
            export.save_attachement('csv', tags['file'], tags['ftp'] or
                                    tags['disk'])

    def save_attachement(self, type, content, filename, inc=None):
        ira = self.env['ir.attachment']

        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = filename + timestr + '.csv'

        values = {
            'name': filename,
            'datas_fname': filename,
            'res_model': 'csv.export.manager',
            'res_id': self.id,
            'type': 'binary',
            'public': True,
            'datas': base64.b64encode(content.getvalue()),
        }
        ira.create(values)
