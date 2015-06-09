# -*- encoding: utf-8 -*-
# ! python2

"""
Working with temporary data.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os
from time import gmtime, strftime

from django.conf import settings

from ..funcs import id_generator


class TmpStorage(object):
    """
    This helper covers operations with processes temporary files.
    """

    @staticmethod
    def make_path(tracker_storage_path):
        """
        Make path if path doesn't exist.

        :param tracker_storage_path: Path to create
        :return: True if path was created otherwise False
        """
        if not os.path.exists(tracker_storage_path):
            os.makedirs(tracker_storage_path)
            return True

        return False

    @staticmethod
    def get_write_dir(sub_dir=None):

        if not sub_dir:
            sub_dir = id_generator()

        tracker_storage_path = os.path.join(settings.PROCESS_TMP_STORAGE, sub_dir)
        TmpStorage.make_path(tracker_storage_path)

        return tracker_storage_path

    @staticmethod
    def get_filename_with_today(filename, extension):
        today_date = strftime("%Y-%m-%d", gmtime())
        filename = "{0}_{1}.{2}".format(today_date, filename, extension)

        return filename