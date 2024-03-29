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

from qpc_tools import messages
from qpc_tools import server
from qpc_tools.clicommand import CliCommand
from qpc_tools.release import DOWNSTREAM
from qpc_tools.translation import _
from qpc_tools.utils import (BOOLEAN_CHOICES,
                             check_abs_paths,
                             create_ansible_command)


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
        if DOWNSTREAM:
            # Be careful adding defaults here, because it would require a new
            # upstream release to change the downstream defaults.
            self.parser.add_argument('--registry-no-auth', dest='registry_no_auth',
                                     action='store_true',
                                     help=_(messages.SERVER_INSTALL_REGISTRY_NO_AUTH_HELP),
                                     required=False)
            self.parser.add_argument('--registry-url', dest='registry_url',
                                     default='registry.redhat.io',
                                     help=_(messages.SERVER_INSTALL_REGISTRY_URL_HELP),
                                     required=False)
            self.parser.add_argument('--registry-user', dest='registry_username',
                                     help=_(messages.SERVER_INSTALL_REGISTRY_UN_HELP),
                                     required=False)
            self.parser.add_argument('--registry-password', dest='registry_password',
                                     help=_(messages.SERVER_INSTALL_REGISTRY_PASS_HELP),
                                     required=False)
            self.parser.add_argument('--server-image-name', dest='server_image_name',
                                     help=_(messages.SERVER_INSTALL_SERVER_IMAGE_HELP),
                                     required=False)
            self.parser.add_argument('--db-image-name', dest='db_image_name',
                                     help=_(messages.SERVER_INSTALL_DB_IMAGE_HELP),
                                     required=False)
        else:
            # Upstream only args
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
        self.parser.add_argument('--db-user', dest='db_user',
                                 default='postgres',
                                 help=_(messages.SERVER_INSTALL_DB_USER_HELP),
                                 required=False)
        self.parser.add_argument('--db-password', dest='db_password',
                                 help=_(messages.SERVER_INSTALL_DB_PASSWORD_HELP),
                                 required=False)
        self.parser.add_argument('--username', dest='server_username',
                                 default='admin',
                                 help=_(messages.SERVER_INSTALL_USERNAME_HELP),
                                 required=False)
        self.parser.add_argument('--password', dest='server_password',
                                 help=_(messages.SERVER_INSTALL_PASSWORD_HELP),
                                 required=False)
        self.parser.add_argument('--advanced', dest='server_advanced',
                                 nargs='+', default=[],
                                 help=SUPPRESS,
                                 required=False)

    def _validate_args(self):
        """Sub-commands can override."""
        check_abs_paths(self.args)

    def _do_command(self):
        """Install the server."""
        # Can't use subprocess.run cause python > 3.5
        cwd_abs_path = os.path.abspath(os.path.dirname(__file__))
        playbook_abs_path = os.path.join(cwd_abs_path, server.SERVER_INSTALL_PLAYBOOK)
        ansible_command = create_ansible_command(self.args, playbook_abs_path)
        try:
            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                ansible_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE
            )
            for line in iter(process.stdout.readline, b''):
                format_line = line.decode('utf-8').strip('\n')
                print(format_line)
            # process.communicate performs a wait until playbooks is done
            stderr_data = process.communicate()[1]
            code = process.returncode
            if code == 0:
                print(_(messages.SERVER_INSTALLATION_SUCCESSFUL))
            else:
                print(_(messages.SERVER_INSTALLATION_FAILED))
                if stderr_data != b'':
                    format_stderr = stderr_data.decode('utf-8').strip('\n')
                    if 'WARNING' not in format_stderr:
                        print(_(messages.INSTALL_ERROR_MESSAGE % format_stderr))
        except ValueError:
            print(_(messages.SERVER_INSTALLATION_FAILED))
        except KeyboardInterrupt:
            print(_(messages.INSTALLATION_CANCELED))
