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

from argparse import SUPPRESS

import qpc_tools.install as install
from qpc_tools import messages
from qpc_tools.clicommand import CliCommand
from qpc_tools.translation import _


# pylint: disable=too-few-public-methods
class InstallCLICommand(CliCommand):
    """Defines the install CLI command."""

    SUBCOMMAND = install.SUBCOMMAND
    ACTION = install.CLI

    def __init__(self, subparsers):
        """Create command."""
        # pylint: disable=no-member
        CliCommand.__init__(self, self.SUBCOMMAND, self.ACTION,
                            subparsers.add_parser(self.ACTION))
        self.parser.add_argument('--offline', dest='offline',
                                 choices=install.BOOLEAN_CHOICES,
                                 default='false',
                                 help=_(messages.CLI_INSTALL_OFFLINE_HELP),
                                 required=False)
        self.parser.add_argument('--offline-files', dest='offline_files',
                                 help=_(messages.CLI_INSTALL_OFFLINE_FILES_HELP),
                                 required=False)
        self.parser.add_argument('--version', dest='version',
                                 default='latest',
                                 help=_(messages.CLI_INSTALL_VERSION_HELP),
                                 required=False)
        self.parser.add_argument('--home-dir', dest='home_dir',
                                 default='~/quipucords',
                                 help=_(messages.INSTALL_HOME_DIR_HELP),
                                 required=False)
        self.parser.add_argument('--server-hostname', dest='server_host',
                                 default='127.0.0.1',
                                 help=_(messages.CLI_INSTALL_SERVER_HELP),
                                 required=False)
        self.parser.add_argument('--server-port', dest='server_port',
                                 default='9443',
                                 help=_(messages.CLI_INSTALL_SERVER_PORT_HELP),
                                 required=False)
        self.parser.add_argument('--extra', dest='extra',
                                 help=SUPPRESS,
                                 required=False)

    def _do_command(self):
        """Install the CLI."""
        print(_(messages.CLI_INSTALLATION_SUCCESSFUL))
