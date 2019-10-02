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
"""QPC Tools Command Line Interface."""

from __future__ import print_function

from argparse import ArgumentParser


from qpc_tools import cli, messages, server
from qpc_tools.cli.commands import InstallCLICommand
from qpc_tools.release import VERSION
from qpc_tools.server.commands import InstallServerCommand
from qpc_tools.translation import _
from qpc_tools.utils import (ensure_config_dir_exists,
                             ensure_data_dir_exists,
                             setup_logging)


# pylint: disable=too-few-public-methods
class CLI():
    """Defines the CLI class.

    Class responsible for displaying usage or matching inputs
    to the valid set of commands supported by qpc-tools.
    """

    def __init__(self, name='cli_main', usage=None, shortdesc=None,
                 description=None):
        """Create main command line handler."""
        self.shortdesc = shortdesc
        if shortdesc is not None and description is None:
            description = shortdesc
        self.parser = ArgumentParser(usage=usage, description=description)
        self.parser.add_argument('--version', action='version',
                                 version=VERSION)
        self.parser.add_argument('-v', dest='verbosity', action='count',
                                 default=0, help=_(messages.VERBOSITY_HELP))
        self.subparsers = self.parser.add_subparsers(dest='subcommand')
        self.name = name
        self.args = None
        self.subcommands = {}
        self._add_subcommand(cli.SUBCOMMAND,
                             [InstallCLICommand])
        self._add_subcommand(server.SUBCOMMAND,
                             [InstallServerCommand])
        ensure_data_dir_exists()
        ensure_config_dir_exists()

    def _add_subcommand(self, subcommand, actions):
        subcommand_parser = self.subparsers.add_parser(subcommand)
        action_subparsers = subcommand_parser.add_subparsers(dest='action')
        self.subcommands[subcommand] = {}
        for action in actions:
            action_inst = action(action_subparsers)
            action_dic = self.subcommands[action.SUBCOMMAND]
            action_dic[action.ACTION] = action_inst

    def main(self):
        """Execute of subcommand operation.

        Method determine whether to display usage or pass input
        to find the best command match. If no match is found the
        usage is displayed
        """
        self.args = self.parser.parse_args()
        setup_logging(self.args.verbosity)

        if self.args.subcommand in self.subcommands:
            subcommand = self.subcommands[self.args.subcommand]
            if self.args.action in subcommand:
                action = subcommand[self.args.action]
                action.main(self.args)
            else:
                self.parser.print_help()
        else:
            self.parser.print_help()
