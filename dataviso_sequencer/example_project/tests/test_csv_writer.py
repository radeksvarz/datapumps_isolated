# -*- encoding: utf-8 -*-
# ! python2

# from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import codecs
import os

from django.test import TestCase
from nose.tools import assert_raises

from dataviso_sequencer.lib.csv_utils import CsvWriter


class CSVWriterTestCase(TestCase):
    TMP_FILE_NAME = "csv_writer_test.tmp"

    def setUp(self):
        super(CSVWriterTestCase, self).setUpClass()

        open(self.TMP_FILE_NAME, 'a').close()

    def test_CsvWriter(self):
        value = u'7.4.3 \u2013 Sybase'

        with open(self.TMP_FILE_NAME, 'wb') as the_file:
            writer = CsvWriter(the_file)

            self.assertRaises(UnicodeEncodeError, writer.write_row, [value])

        with codecs.open(self.TMP_FILE_NAME, 'wb', encoding='utf-8') as the_file:
            writer = CsvWriter(the_file)

            with assert_raises(UnicodeEncodeError) as cm:
                writer.write_row([str(value)])

            writer.write_row([value])

        with open(self.TMP_FILE_NAME, 'r') as the_file:
            assert the_file.read().decode('utf-8').startswith(CsvWriter.DIALECT.quotechar + value)

    @classmethod
    def tearDownClass(cls):
        super(CSVWriterTestCase, cls).tearDownClass()

        os.unlink(cls.TMP_FILE_NAME)
