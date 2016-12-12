# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import logging

import paramiko

from openerp.addons.server_environment import serv_config
# from openerp.osv.orm import except_orm
# from openerp import exceptions

SERV_CONFIG_SECTION = 'sftp_csv'
_logger = logging.getLogger('SFTP')

# Paramiko sftp client doc on
# http://docs.paramiko.org/en/2.0/api/sftp.html


class _SFTPInterface(object):

    def __init__(self):
        self._server = serv_config.get(SERV_CONFIG_SECTION, 'server')
        self._port = int(serv_config.get(SERV_CONFIG_SECTION, 'port'))
        self._username = serv_config.get(SERV_CONFIG_SECTION, 'username')
        self._password = serv_config.get(SERV_CONFIG_SECTION, 'password')
        self._ssh_client = None
        self._sftp_client = None

    def _open_sftp_client(self):
        _logger.info('open connection')
        if self._sftp_client:
            return
        if self._server != 'localhost':
            trnsprt = paramiko.Transport((self._server, self._port))
            trnsprt.connect(username=self._username,
                            password=self._password)
            trnsprt.set_keepalive(10)
            self._sftp_client = paramiko.SFTPClient.from_transport(trnsprt)
        else:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )
            self._ssh_client.connect(hostname=self._server,
                                     timeout=3)
            self._ssh_client.get_transport().set_keepalive(10)
            self._sftp_client = self._ssh_client.open_sftp()

    def close(self):
        self._close_sftp_client(True)

    def _close_sftp_client(self, force=False):
        if force and self._sftp_client is not None:
            _logger.info('close connection')
            self._sftp_client.close()
            self._sftp_client = None
            if self._ssh_client:
                self._ssh_client.close()
                self._ssh_client = None

    def save_output_to_sftp(self, output, filename):
        _logger.info('save to %s', filename)
        self._open_sftp_client()
        try:
            self._sftp_client.chdir(os.path.dirname(filename))
        except paramiko.SSHException as exc:
            _logger.error('Error while trying to cd to sftp directory %s: %s',
                          filename, exc)
            _logger.info('Trying to reconnect')
            self._close_sftp_client(force=True)
            self._open_sftp_client()
            self._sftp_client.chdir(os.path.dirname(filename))
        self._sftp_client.putfo(output, os.path.basename(filename))

        self._close_sftp_client()

    def get_file_list_from_sftp(self, filepath):
        _logger.info('ls %s', filepath)
        self._open_sftp_client()

        filename_list = []

        try:
            filepath_content_list = self._sftp_client.listdir(filepath)
        except paramiko.SSHException as exc:
            _logger.error('Error while trying to list sftp directory %s: %s',
                          filepath, exc)
            _logger.info('Trying to reconnect')
            self._close_sftp_client(force=True)
            self._open_sftp_client()
            filepath_content_list = self._sftp_client.listdir(filepath)

        for content in filepath_content_list:
            lstat = self._sftp_client.lstat(filepath + content)
            if 'd' not in str(lstat).split()[0]:
                filename_list.append(content)

        self._close_sftp_client()

        return filename_list

    def move_files_on_sftp(self, files, destination_path):
        _logger.info('mv %s %s', files, destination_path)
        self._open_sftp_client()

        for sftp_file in files:
            self._sftp_client.rename(
                sftp_file, destination_path + os.path.basename(sftp_file)
            )

        self._close_sftp_client()

    def read_file(self, filename):
        _logger.info('read %s', filename)
        self._open_sftp_client()

        opened_file = self._sftp_client.open(filename, mode='r')
        file_content = opened_file.read()
        opened_file.close()

        self._close_sftp_client()

        return file_content

    def __del__(self):
        self.close()


_interface = None


def SFTPInterface():
    global _interface
    if _interface is None:
        _interface = _SFTPInterface()
    return _interface
