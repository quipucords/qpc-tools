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

from qpc_tools.release import PYTHON_SRC_PATH

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
    """Build Ansible Command."""
    # Initial command setup
    cmd_list = ['ansible-playbook']
    # print(PYTHON_SRC_PATH)
    # print(playbook)
    # playbook_path = '%s/%s' % (PYTHON_SRC_PATH, playbook)
    cmd_list.append(playbook)
    verbosity_lvl = '-vv'
    cmd_list.append(verbosity_lvl)
    # Fiter Extra Vars
    extra_vars = namespace_args.__dict__
    for key in NOT_ANSIBLE_KEYS:
        if key in extra_vars.keys():
            extra_vars.pop(key, None)
    extra_vars = {k: v for k, v in extra_vars.items() if v is not None}
    # Add extra vars to command
    extra_format = '-e %s=%s'
    for key, value in extra_vars.items():
        extra_var = extra_format % (key, value)
        cmd_list.append(extra_var)
    return cmd_list
