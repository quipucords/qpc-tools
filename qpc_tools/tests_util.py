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
"""Test the Utils module."""

import logging
import unittest

from qpc_tools import utils


class UtilsTests(unittest.TestCase):
    """Class for testing the utils."""

    def test_setup_logging_info(self):
        """Testing the utils info logging."""
        utils.setup_logging(utils.LOG_LEVEL_INFO)
        log = logging.getLogger('qpc_tools')
        self.assertEqual(log.level, logging.INFO)

    def test_setup_logging_debug(self):
        """Testing the utils debug loggins."""
        utils.setup_logging(logging.DEBUG)
        log = logging.getLogger('qpc_tools')
        self.assertEqual(log.level, logging.DEBUG)
