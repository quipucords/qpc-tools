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
"""Test the Install CLI module."""

import sys
import unittest
from argparse import ArgumentParser, Namespace  # noqa: I100
from io import StringIO

from qpc_tools import messages
from qpc_tools.install.cli import InstallCLICommand
from qpc_tools.tests_utilities import HushUpStderr, redirect_stdout
from qpc_tools.translation import _


PARSER = ArgumentParser()
SUBPARSER = PARSER.add_subparsers(dest='subcommand')


class CredentialAddCliTests(unittest.TestCase):
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

    def test_install_all_success(self):
        """Testing the installation of CLI command was successful."""
        cred_out = StringIO()
        cac = InstallCLICommand(SUBPARSER)
        args = Namespace()
        with redirect_stdout(cred_out):
            cac.main(args)
            self.assertEqual(cred_out.getvalue().strip(),
                             _(messages.CLI_INSTALLATION_SUCCESSFUL))
