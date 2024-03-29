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
"""qpc tools command line utilities."""

from __future__ import print_function

import logging
import os
import sys
from collections import OrderedDict
from getpass import getpass

from qpc_tools import messages
from qpc_tools.release import DOWNSTREAM
from qpc_tools.translation import _


QPC_PATH = 'qpc_tools'
CONFIG_HOME_PATH = '~/.config/'
DATA_HOME_PATH = '~/.local/share/'
CONFIG_HOME = os.path.expanduser(CONFIG_HOME_PATH)
DATA_HOME = os.path.expanduser(DATA_HOME_PATH)
CONFIG_DIR = os.path.join(CONFIG_HOME, QPC_PATH)
DATA_DIR = os.path.join(DATA_HOME, QPC_PATH)
QPC_LOG = os.path.join(DATA_DIR, 'qpc-tools.log')
QPC_SERVER_CONFIG = os.path.join(CONFIG_DIR, 'qpc-tools.config')

LOG_LEVEL_INFO = 0

BOOLEAN_CHOICES = ['True', 'False', 'true', 'false']
NOT_ANSIBLE_KEYS = ['action', 'subcommand', 'verbosity']

# pylint: disable=invalid-name
logging.captureWarnings(True)
log = logging.getLogger('qpc_tools')


def ensure_config_dir_exists():
    """Ensure the qpc tools configuration directory exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def ensure_data_dir_exists():
    """Ensure the qpc tools data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def setup_logging(verbosity):
    """Set up Python logging for qpc tools.

    Must be run after ensure_data_dir_exists().

    :param verbosity: verbosity level, as measured in -v's on the command line.
        Can be None for default.
    """
    ensure_data_dir_exists()
    if verbosity == LOG_LEVEL_INFO:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    # Using basicConfig here means that all log messages, even
    # those not coming from qpc tools, will go to the log file
    logging.basicConfig(filename=QPC_LOG, format='%(asctime)s - %(name)s - '
                                                 '%(levelname)s - %(message)s')
    # but we only adjust the log level for the 'qpc-tools' logger.
    log.setLevel(log_level)
    # the StreamHandler sends warnings and above to stdout, but
    # only for messages going to the 'qpc-tools' logger, i.e. qpc-tools
    # output.
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.ERROR)
    log.addHandler(stderr_handler)


def log_args(args):
    """Log the arguments for each qpc-tools command.

    :param args: the arguments provided to the qpc-tools command
    """
    message = 'Args: "%s"'
    log.info(message, args)


def create_ansible_command(namespace_args, playbook):
    """Build Ansible Command.

    :param namespace_args: arguments passed in by the user
    :param playbook: name of the playbook
    :returns:  The ansible command that will be run
    """
    # Initial command setup
    cmd_list = ['ansible-playbook']
    cmd_list.append(playbook)
    verbosity_lvl = '-vv'
    cmd_list.append(verbosity_lvl)
    # Filter Extra Vars
    args_dictionary = check_offline(namespace_args.__dict__)
    install_vars = get_password(args_dictionary)
    for key in NOT_ANSIBLE_KEYS:
        if key in install_vars.keys():
            install_vars.pop(key, None)
    # grab the advanced args
    advanced_args = install_vars.pop('server_advanced', []) or []
    install_vars = {k: v for k, v in install_vars.items() if v is not None}
    # Add extra vars to command
    extra_format = '-e %s=%s'
    for key, value in install_vars.items():
        extra_var = extra_format % (key, value)
        cmd_list.append(extra_var)
    # loop through advanced args and add them to the command
    for advanced_cmd in advanced_args:
        cmd_list.append(f'-e {advanced_cmd}')
    # print command and mask passwords
    tmp_list = cmd_list.copy()
    for arg in tmp_list:
        if 'password' in arg:
            mask_arg = arg.split('=')[0] + '=' + '*******'
            tmp_list.remove(arg)
            tmp_list.append(mask_arg)
    print(_(messages.PLAYBOOK_COMMAND % (' '.join(tmp_list))))
    return cmd_list


def make_path_absolute(path):
    """Check and convert all paths to an absolute path.

    :param path: (str) path that may be relative or absolute
    :returns: (str) path that will be absolute
    """
    abs_path = path
    if '~' in abs_path:
        abs_path = os.path.expanduser(abs_path)
    abs_path = os.path.abspath(abs_path)
    return abs_path


def check_abs_paths(args):
    """Check and convert all paths to an absolute path.

    :param path: (args) commands arguments
    :returns: None
    """
    if not DOWNSTREAM:
        if args.offline_files:
            abs_offline_files = make_path_absolute(args.offline_files)
            if not os.path.exists(abs_offline_files):
                print(_(messages.ALL_DIRECTORY_DOES_NOT_EXIST %
                        ('offline-files', abs_offline_files)))
                sys.exit(1)
            args.offline_files = abs_offline_files
    if args.home_dir:
        args.home_dir = make_path_absolute(args.home_dir)


def get_password(args_dictionary):
    """Collect the password value and place in the args dictionary.

    :param args_dictionary: the dictionary containing the args and values
    :returns: the dictionary with updated passwords
    """
    if args_dictionary.get('registry_no_auth'):
        arg_prompt = OrderedDict([
            ('server_password', 'Enter server password: '),
            ('db_password', 'Enter database password: ')
        ])
    else:
        registry_url = args_dictionary.get('registry_url')
        arg_prompt = OrderedDict([
            ('registry_username', f'Enter {registry_url} username: '),
            ('registry_password', f'Enter {registry_url} password: '),
            ('server_password', 'Enter server password: '),
            ('db_password', 'Enter database password: ')
        ])
    for arg, prompt in arg_prompt.items():
        if arg in args_dictionary and args_dictionary[arg] is None:
            if arg == 'registry_username':
                arg_value = input(prompt)
            else:
                arg_value = None
                count = 0
                while arg_value in [None, ''] and count < 3:
                    arg_value = getpass(prompt=prompt)
                    count += 1
                if count >= 3:
                    sys.exit('Exiting due to failure to enter password.')
            args_dictionary[arg] = arg_value

    return args_dictionary


def check_offline(args_dictionary):
    """Check if offline_files exists and add offline arg."""
    if args_dictionary.get('offline_files') is not None:
        args_dictionary['install_offline'] = True
    return args_dictionary
