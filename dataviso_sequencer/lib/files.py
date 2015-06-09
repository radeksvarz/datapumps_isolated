# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from django.core.files.base import ContentFile

from ..lib.isolated_filesystem import TmpStorage


class TimestampedContentFile(ContentFile):
    def __init__(self, content, name, extension):
        name = TmpStorage.get_filename_with_today(name, extension)

        super(TimestampedContentFile, self).__init__(content, name)