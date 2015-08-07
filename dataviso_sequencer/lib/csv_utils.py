# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import csv


class CsvWriter(object):
    """
    Unicode-friendly CSV writer
    """
    DIALECT = csv.excel

    def __init__(self, csv_file, delimiter=DIALECT.delimiter):
        self.csv_file = csv_file
        self.delimiter = delimiter

    def write_row(self, row):
        values = [unicode(v) if not isinstance(v, unicode) else v for v in row]
        values = [u'{0}{1}{0}'.format(self.DIALECT.quotechar, v) for v in values]
        line = self.delimiter.join(values) + self.DIALECT.lineterminator

        self.csv_file.write(line)
