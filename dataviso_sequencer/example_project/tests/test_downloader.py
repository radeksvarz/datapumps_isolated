# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from django.test import TestCase

from dataviso_sequencer.steps.downloader import Downloader


class DownloaderTestCase(TestCase):
    def setUp(self):
        self.downloader = Downloader()

    def test_valid_filenames_return_True(self):
        valid_filenames = [
            "foo.html",
            "bar.baz.pdf",
            "abc.JPG"
        ]

        for filename in valid_filenames:
            self.assertTrue(self.downloader.validate_filename(filename))

    def test_invalid_filenames_return_False(self):
        invalid_filenames = [
            "foo",
            "",
        ]

        for filename in invalid_filenames:
            self.assertFalse(self.downloader.validate_filename(filename))

    def test_downloader_can_download_url(self):
        self.downloader.download_url("http://www.example.com", "test_downloaded_page.html")

    def test_download_url_accept_only_html_filename(self):
        self.assertRaises(ValueError, self.downloader.download_url, "http://www.example.com", "INVALID_FILENAME.pdf")
