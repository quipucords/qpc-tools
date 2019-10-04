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
"""InstallServerCommand is used to install the server."""

from __future__ import print_function

import os
import subprocess
from argparse import SUPPRESS

import qpc_tools.server as server
from qpc_tools import messages
from qpc_tools.clicommand import CliCommand
from qpc_tools.translation import _
from qpc_tools.utils import (BOOLEAN_CHOICES,
                             create_ansible_command,
                             validate_and_update_paths)


# pylint: disable=too-few-public-methods
class InstallServerCommand(CliCommand):
    """Defines the install server command."""

    SUBCOMMAND = server.SUBCOMMAND
    ACTION = server.INSTALL

    def __init__(self, subparsers):
        """Create command."""
        # pylint: disable=no-member
        CliCommand.__init__(self, self.SUBCOMMAND, self.ACTION,
                            subparsers.add_parser(self.ACTION))
        self.parser.add_argument('--offline', dest='install_offline',
                                 action='store_true',
                                 help=_(messages.SERVER_INSTALL_OFFLINE_HELP),
                                 required=False)
        self.parser.add_argument('--offline-files', dest='offline_files',
                                 help=_(messages.SERVER_INSTALL_OFFLINE_FILES_HELP),
                                 required=False)
        self.parser.add_argument('--version', dest='server_version',
                                 help=_(messages.SERVER_INSTALL_VERSION_HELP),
                                 required=False)
        self.parser.add_argument('--home-dir', dest='home_dir',
                                 help=_(messages.ALL_INSTALL_HOME_DIR_HELP),
                                 required=False)
        self.parser.add_argument('--port', dest='server_port',
                                 default='9443',
                                 help=_(messages.SERVER_INSTALL_PORT_HELP),
                                 required=False)
        self.parser.add_argument('--open-port', dest='open_port',
                                 choices=BOOLEAN_CHOICES,
                                 default='true',
                                 help=_(messages.SERVER_INSTALL_OPEN_PORT_HELP),
                                 required=False)
        self.parser.add_argument('--dbms-user', dest='dbms_user',
                                 default='postgres',
                                 help=_(messages.SERVER_INSTALL_DBMS_USER_HELP),
                                 required=False)
        self.parser.add_argument('--dbms-password', dest='dbms_password',
                                 help=_(messages.SERVER_INSTALL_DBMS_PASSWORD_HELP),
                                 required=False)
        self.parser.add_argument('--username', dest='server_username',
                                 default='admin',
                                 help=_(messages.SERVER_INSTALL_USERNAME_HELP),
                                 required=False)
        self.parser.add_argument('--password', dest='server_password',
                                 help=_(messages.SERVER_INSTALL_PASSWORD_HELP),
                                 required=False)
        self.parser.add_argument('--advanced', dest='server_advanced',
                                 help=SUPPRESS,
                                 required=False)

    def _validate_args(self):
        """Sub-commands can override."""
        validate_and_update_paths(self.args)

    def _do_command(self):
        """Install the server."""
        # Can't use subprocess.run cause python > 3.5
        cwd_abs_path = os.path.abspath(os.path.dirname(__file__))
        playbook_abs_path = os.path.join(cwd_abs_path, server.SERVER_INSTALL_PLAYBOOK)
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
                print(_(messages.SERVER_INSTALLATION_SUCCESSFUL))
            else:
                print(_(messages.SERVER_INSTALLATION_FAILED))
        except ValueError:
            print(_(messages.SERVER_INSTALLATION_FAILED))
