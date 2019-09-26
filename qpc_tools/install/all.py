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
"""InstallAllCommand is used install both the CLI and server."""

from __future__ import print_function

import qpc_tools.install as install
from qpc_tools import messages
from qpc_tools.clicommand import CliCommand
from qpc_tools.translation import _


# pylint: disable=too-few-public-methods
class InstallAllCommand(CliCommand):
    """Defines the install server and CLI command."""

    SUBCOMMAND = install.SUBCOMMAND
    ACTION = install.ALL

    def __init__(self, subparsers):
        """Create command."""
        # pylint: disable=no-member
        CliCommand.__init__(self, self.SUBCOMMAND, self.ACTION,
                            subparsers.add_parser(self.ACTION))

    def _do_command(self):
        """Install the server and CLI."""
        print(_(messages.ALL_INSTALLATION_SUCCESSFUL))
