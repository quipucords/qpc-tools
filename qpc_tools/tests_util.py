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
import unittest
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
        playbook = CLI_INSTALL_PLAYBOOK
        base_online_install = Namespace(action='cli', cli_version=None,
                                        home_dir='~/quipucords', install_offline='false',
                                        offline_files=None, server_advanced=None,
                                        server_host='127.0.0.1', server_port='9443',
                                        subcommand='install', verbosity=0)
        success_online = ['ansible-playbook', '/%s' % CLI_INSTALL_PLAYBOOK,
                          '-vv', '-e home_dir=~/quipucords', '-e install_offline=false',
                          '-e server_host=127.0.0.1', '-e server_port=9443']

        cmd_list = utils.create_ansible_command(base_online_install, playbook)
        for cmd_part in cmd_list:
            self.assertIn(cmd_part, success_online)
        playbook = SERVER_INSTALL_PLAYBOOK
        base_online_install = Namespace(action='server', dbms_password=None,
                                        dbms_user='postgres', home_dir='~/quipucords',
                                        install_offline='false', offline_files=None,
                                        open_port='true', server_advanced=None,
                                        server_password=None, server_port='9443',
                                        server_username='admin', server_version=None,
                                        subcommand='install', verbosity=0)
        success_online = ['ansible-playbook', '/%s' % SERVER_INSTALL_PLAYBOOK,
                          '-vv', '-e install_offline=false', '-e home_dir=~/quipucords',
                          '-e server_port=9443', '-e open_port=true', '-e dbms_user=postgres',
                          '-e server_username=admin']
        cmd_list = utils.create_ansible_command(base_online_install, playbook)
        for cmd_part in cmd_list:
            self.assertIn(cmd_part, success_online)
