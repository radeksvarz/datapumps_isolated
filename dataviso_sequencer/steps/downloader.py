# -*- encoding: utf-8 -*-
# ! python2

"""
Downloaders base class.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta
import os
from tempfile import NamedTemporaryFile
import shutil
import re

from misc_filename_utils.funcs import get_filename_from_url

from django.core.validators import URLValidator
import requests

from ..lib.isolated_filesystem import TmpStorage
from ..lib.core import Step


class Downloader(Step):
    __metaclass__ = ABCMeta
    key = "downloader"

    def __init__(self):
        super(Downloader, self).__init__()

    def get_output(self):
        raise NotImplementedError()

    def validate_filename(self, filename):
        regex = re.compile("^[\w,\._\s-]+\.[A-Za-z]{1,10}$", re.IGNORECASE)
        r = regex.search(filename)

        if r:
            return True
        else:
            return False

    def download_url(self, url, filename):
        """
        Alias for `download_file`.

        :param url: URL to download
        :param filename: Target filename, this name should ends with ".html"
        :return: Downloaded file
        :raise ValueError: If given filename is not valid.
        """
        if not filename.endswith(".html"):
            raise ValueError("Target filename for URL should ends with `.html` extension.")

        return self.download_file(url, filename)

    def download_file(self, url, filename=None):
        """
        Download file from remote location, save downloaded file locally and return it.

        :param url: URL pointing to a file.
        :type url: str or unicode_literals
        :return: Downloaded file object.
        :rtype: file
        """

        # Is given URL valid?
        URLValidator()(url)

        local_filename = get_filename_from_url(url) if not filename else filename

        if not self.validate_filename(local_filename):
            raise ValueError("`%s` is not a valid filename." % local_filename)

        # NOTE the stream=True parameter, this enables chunks
        http_request = requests.get(url, stream=True)

        tmp_file = NamedTemporaryFile(delete=False)

        with tmp_file as file_context:
            for chunk in http_request.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    file_context.write(chunk)
                    file_context.flush()

        target = os.path.join(TmpStorage.get_write_dir(self.key), local_filename)
        shutil.copy(tmp_file.name, target)

        os.remove(tmp_file.name)

        return target
