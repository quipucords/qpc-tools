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
"""Test the install module utilities."""


import sys
import unittest
from argparse import Namespace  # noqa: I100

from qpc_tools.install.utils import create_ansible_command
from qpc_tools.tests_utilities import HushUpStderr


class InstallCLICommandTests(unittest.TestCase):
    """Class for testing the install CLI commands."""

    def setUp(self):
        """Create test setup."""
        # Temporarily disable stderr for these tests, CLI errors clutter up
        # nosetests command.
        self.orig_stderr = sys.stderr
        sys.stderr = HushUpStderr()

    def tearDown(self):
        """Remove test setup."""
        # Restore stderr
        sys.stderr = self.orig_stderr

    def test_ansible_command_cli(self):
        """Testing ansible command creation."""
        playbook = 'cli/cli_playbook.yml'
        base_online_install = Namespace(action='cli', cli_version=None,
                                        home_dir='~/quipucords', install_offline='false',
                                        offline_files=None, server_advanced=None,
                                        server_host='127.0.0.1', server_port='9443',
                                        subcommand='install', verbosity=0)
        success_online = ['ansible-playbook', '/cli/cli_playbook.yml',
                          '-vv', '-e home_dir=~/quipucords', '-e install_offline=false',
                          '-e server_host=127.0.0.1', '-e server_port=9443']

        cmd_list = create_ansible_command(base_online_install, playbook)
        for cmd_part in cmd_list:
            self.assertIn(cmd_part, success_online)
        playbook = 'server/server_playbook.yml'
        base_online_install = Namespace(action='server', dbms_password=None,
                                        dbms_user='postgres', home_dir='~/quipucords',
                                        install_offline='false', offline_files=None,
                                        open_port='true', server_advanced=None,
                                        server_password=None, server_port='9443',
                                        server_username='admin', server_version=None,
                                        subcommand='install', verbosity=0)
        success_online = ['ansible-playbook', '/server/server_playbook.yml',
                          '-vv', '-e install_offline=false', '-e home_dir=~/quipucords',
                          '-e server_port=9443', '-e open_port=true', '-e dbms_user=postgres',
                          '-e server_username=admin']
        cmd_list = create_ansible_command(base_online_install, playbook)
        for cmd_part in cmd_list:
            self.assertIn(cmd_part, success_online)
