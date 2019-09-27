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
#

"""QPC Tools messages for translation."""
VERBOSITY_HELP = 'Verbose mode. Use up to -vvvv for more verbosity.'

INSTALL_HOME_DIR_HELP = 'The home directory for the Quipucords applications '\
    'to store data (defaults to ~/quipucords)'

ALL_INSTALLATION_SUCCESSFUL = 'Installation of both server and CLI was successful'

SERVER_INSTALLATION_SUCCESSFUL = 'Installation of server was successful'
SERVER_INSTALL_OFFLINE_HELP = 'Perform an offline Server installation (defaults to false)'
SERVER_INSTALL_OFFLINE_FILES_HELP = 'Specify the path to the server offline files'
SERVER_INSTALL_VERSION_HELP = 'Specify the QPC Server version to install '\
    '(defaults to latest release)'
SERVER_INSTALL_PORT_HELP = 'Port number of the server (defaults to 9443)'
SERVER_INSTALL_OPEN_PORT_HELP = "Indicate whether the host machine's port should be' \
    'opened (defaults to true)"
SERVER_INSTALL_DBMS_USER_HELP = 'Set the PostgreSQL db user (defaults to postgres)'
SERVER_INSTALL_DBMS_PASSWORD_HELP = 'Set the PostgreSQL db password'
SERVER_INSTALL_USERNAME_HELP = 'Set the server admin username (defaults to admin)'
SERVER_INSTALL_PASSWORD_HELP = 'Set the server admin password'

CLI_INSTALLATION_SUCCESSFUL = 'Installation of CLI was successful'
CLI_INSTALL_OFFLINE_HELP = 'Perform an offline CLI installation (defaults to false)'
CLI_INSTALL_OFFLINE_FILES_HELP = 'Specify the path to the CLI offline files'
CLI_INSTALL_VERSION_HELP = 'Specify the QPC CLI version to install (defaults to latest release)'
CLI_INSTALL_SERVER_HELP = 'Host or IP address for the server (defaults to 127.0.0.1)'
CLI_INSTALL_SERVER_PORT_HELP = 'Port number of the server (defaults to 9443)'
