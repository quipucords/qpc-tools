#
# Copyright (c) 2019 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#
"""Test the Utils module."""

import logging
import os
import unittest
from unittest import mock
from argparse import Namespace  # noqa: I100

from qpc_tools import utils
from qpc_tools.cli import CLI_INSTALL_PLAYBOOK
from qpc_tools.server import SERVER_INSTALL_PLAYBOOK


class UtilsTests(unittest.TestCase):
    """Class for testing the utils."""

    def test_setup_logging_info(self):
        """Testing the utils info logging."""
        utils.setup_logging(utils.LOG_LEVEL_INFO)
        log = logging.getLogger('qpc_tools')
        self.assertEqual(log.level, logging.INFO)

    def test_setup_logging_debug(self):
        """Testing the utils debug loggins."""
        utils.setup_logging(logging.DEBUG)
        log = logging.getLogger('qpc_tools')
        self.assertEqual(log.level, logging.DEBUG)

    def test_ansible_command_cli(self):
        """Testing ansible command creation."""
        cwd_abs_path = os.path.abspath(os.path.dirname(__file__))
        cli_path = os.path.join(cwd_abs_path, 'cli/')
        server_path = os.path.join(cwd_abs_path, 'server/')
        playbook = os.path.join(cli_path, CLI_INSTALL_PLAYBOOK)
        base_online_install = Namespace(action='cli', cli_version=None,
                                        home_dir='~/quipucords', install_offline='false',
                                        offline_files=None, server_advanced=None,
                                        server_host='127.0.0.1', server_port='9443',
                                        subcommand='install', verbosity=0,
                                        server_password='qpcpassw0rd',
                                        db_password='password')
        success_online = ['ansible-playbook', playbook,
                          '-vv', '-e home_dir=~/quipucords', '-e install_offline=false',
                          '-e server_host=127.0.0.1', '-e server_port=9443',
                          '-e server_password=qpcpassw0rd', '-e db_password=password']

        cmd_list = utils.create_ansible_command(base_online_install, playbook)
        for cmd_part in cmd_list:
            self.assertIn(cmd_part, success_online)
        playbook = os.path.join(server_path, SERVER_INSTALL_PLAYBOOK)
        base_online_install = Namespace(action='server',
                                        db_user='postgres', home_dir='~/quipucords',
                                        install_offline='false', offline_files=None,
                                        open_port='true', server_advanced=None,
                                        server_port='9443', server_username='admin',
                                        server_version=None,
                                        subcommand='install', verbosity=0,
                                        server_password='qpcpassw0rd',
                                        db_password='password')
        success_online = ['ansible-playbook', playbook,
                          '-vv', '-e install_offline=false', '-e home_dir=~/quipucords',
                          '-e server_port=9443', '-e open_port=true', '-e db_user=postgres',
                          '-e server_username=admin',
                          '-e server_password=qpcpassw0rd', '-e db_password=password']
        cmd_list = utils.create_ansible_command(base_online_install, playbook)
        for cmd_part in cmd_list:
            self.assertIn(cmd_part, success_online)

    def test_abs_path_to_abs(self):
        """Test conversion of abs path to abs."""
        test_path = '/foo/bar'
        abs_path = utils.make_path_absolute(test_path)
        self.assertEqual(test_path, abs_path)

    def test_rel_path_to_abs(self):
        """Test conversion of rel path to abs."""
        test_path = './foo/bar'
        abs_path = utils.make_path_absolute(test_path)
        self.assertNotEqual(test_path, abs_path)
        self.assertNotIn('.', abs_path)

    def test_user_rel_path_to_abs(self):
        """Test conversion of user rel path to abs."""
        test_path = '~/foo/bar'
        abs_path = utils.make_path_absolute(test_path)
        self.assertNotEqual(test_path, abs_path)
        self.assertNotIn('~', abs_path)

    def test_validate_dir_does_not_exist(self):
        """Test offline validation when file doesn't exist."""
        test_path = '~/foo/bar'
        args = Namespace(offline_files=test_path)
        with self.assertRaises(SystemExit):
            utils.check_abs_paths(args)

    def test_validate_dir_does_exist(self):
        """Test offline validation when file doesn't exist."""
        test_path = '~'
        args = Namespace(offline_files=test_path, home_dir=test_path)
        utils.check_abs_paths(args)
        # pylint: disable=no-member
        self.assertNotEqual(test_path, args.offline_files)
        self.assertNotEqual(test_path, args.offline_files)
        self.assertNotIn('~', args.home_dir)
        self.assertNotIn('~', args.home_dir)

    @mock.patch('qpc_tools.utils.getpass')
    def test_get_passwords_none(self, getpass):
        """Test replacing passwords with prompt."""
        getpass.return_value = 'pass'
        args_dictionary = {'foo': 'bar',
                           'server_password': None}
        updated_dictionary = utils.get_password(args_dictionary)
        self.assertEqual(updated_dictionary['server_password'], 'pass')

    @mock.patch('qpc_tools.utils.getpass')
    def test_get_passwords(self, getpass):
        """Test that we don't replace pre-existing passwords."""
        getpass.return_value = 'pass'
        args_dictionary = {'foo': 'bar',
                           'server_password': 'qpcpass'}
        updated_dictionary = utils.get_password(args_dictionary)
        self.assertEqual(updated_dictionary['server_password'], 'qpcpass')
