# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from django.test import TestCase

from misc_filename_utils.funcs import get_filename_from_url


class FilenameFromUrlTestCase(TestCase):
    def test_can_extract_filename_from_url(self):
        url = "http://www.example.com/FOO    -bar-Baz.pdf"
        extracted_filename = get_filename_from_url(url)

        self.assertEqual("foo_-bar-baz.pdf", extracted_filename)
