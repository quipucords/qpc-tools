#!/usr/bin/env python
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
"""InstallCLICommand is used to install the CLI."""

from __future__ import print_function

import os
import subprocess
import sys
from argparse import SUPPRESS

import qpc_tools.cli as cli
from qpc_tools import messages
from qpc_tools.clicommand import CliCommand
from qpc_tools.release import DOWNSTREAM
from qpc_tools.translation import _
from qpc_tools.utils import (check_abs_paths,
                             create_ansible_command)

# pylint: disable=too-few-public-methods


class InstallCLICommand(CliCommand):
    """Defines the install CLI command."""

    SUBCOMMAND = cli.SUBCOMMAND
    ACTION = cli.INSTALL

    def __init__(self, subparsers):
        """Create command."""
        # pylint: disable=no-member
        CliCommand.__init__(self, self.SUBCOMMAND, self.ACTION,
                            subparsers.add_parser(self.ACTION))
        if not DOWNSTREAM:
            # Upstream only args
            self.parser.add_argument('--offline-files', dest='offline_files',
                                     help=_(messages.CLI_INSTALL_OFFLINE_FILES_HELP),
                                     required=False)
        self.parser.add_argument('--version', dest='cli_version',
                                 help=_(messages.CLI_INSTALL_VERSION_HELP),
                                 required=False)
        self.parser.add_argument('--home-dir', dest='home_dir',
                                 help=_(messages.ALL_INSTALL_HOME_DIR_HELP),
                                 required=False)
        self.parser.add_argument('--server-host', dest='server_host',
                                 help=_(messages.CLI_INSTALL_SERVER_HELP),
                                 required=False)
        self.parser.add_argument('--server-port', dest='server_port',
                                 help=_(messages.CLI_INSTALL_PORT_HELP),
                                 required=False)
        self.parser.add_argument('--advanced', dest='server_advanced',
                                 help=SUPPRESS,
                                 required=False)

    def _validate_args(self):
        """Sub-commands can override."""
        if (self.args.server_host or self.args.server_port):
            if not (self.args.server_host and self.args.server_port):
                print(_(messages.CLI_INSTALL_MUST_SPECIFY_PORT_AND_HOST))
                sys.exit(1)
            self.args.configure_server = 'true'
        check_abs_paths(self.args)

    def _do_command(self):
        """Install the CLI."""
        # Can't use subprocess.run cause python > 3.5
        cwd_abs_path = os.path.abspath(os.path.dirname(__file__))
        playbook_abs_path = os.path.join(cwd_abs_path, cli.CLI_INSTALL_PLAYBOOK)
        ansible_command = create_ansible_command(self.args, playbook_abs_path)
        try:
            process = subprocess.Popen(ansible_command,
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, b''):
                format_line = line.decode('utf-8').strip('\n')
                print(format_line)
            # process.communicate performs a wait until playbooks is done
            process.communicate()
            code = process.returncode
            if code == 0:
                print(_(messages.CLI_INSTALLATION_SUCCESSFUL))
            else:
                print(_(messages.CLI_INSTALLATION_FAILED))
        except ValueError:
            print(_(messages.CLI_INSTALLATION_FAILED))
