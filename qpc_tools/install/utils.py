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
"""qpc-tools install Command Line utilities."""

from qpc_tools.release import PLAYBOOK_PATH

NOT_ANSIBLE_KEYS = ['action', 'subcommand', 'verbosity']


def create_ansible_command(namespace_args, playbook):
    """Build Ansible Command."""
    # Initial command setup
    cmd_list = ['ansible-playbook']
    playbook_path = '%s/%s' % (PLAYBOOK_PATH, playbook)
    cmd_list.append(playbook_path)
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
