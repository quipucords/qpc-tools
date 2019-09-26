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
"""Base CLI Command Class."""

from __future__ import print_function

from qpc_tools.utils import log_args


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class CliCommand():
    """Base class for all sub-commands."""

    # pylint: disable=too-many-arguments
    def __init__(self, subcommand, action, parser):
        """Create cli command base object."""
        self.subcommand = subcommand
        self.action = action
        self.parser = parser
        self.args = None

    def _validate_args(self):
        """Sub-commands can override."""
        pass

    def _do_command(self):
        """Execute command flow.

        Sub-commands define this method to perform the
        required action once all options have been verified.
        """
        pass

    def main(self, args):
        """Trigger main command flow.

        The method that does a basic check for command
        validity and set's the process in motion.
        """
        self.args = args
        self._validate_args()
        log_args(self.args)

        self._do_command()
