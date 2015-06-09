# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import time

from dataviso_sequencer.types.types import LogSeverity

from ..lib.data import Logger


class TimeStampedLogger(Logger):
    def __init__(self):
        super(TimeStampedLogger, self).__init__()

    def get_current_microseconds(self):
        return time.time() * 1000.0

    def _make_timestamped_line(self, text, severity):
        current_time_with_microseconds = self.get_current_microseconds()

        return [
            {
                'timestamp': current_time_with_microseconds,
                'content': unicode(text),
                'severity': severity
            }
        ]

    def _create_list_for_data(self):
        if not self.data:
            self.data = []

    def warning(self, text):
        self.add_line(text, LogSeverity.WARNING)

    def info(self, text):
        self.add_line(text, LogSeverity.INFO)

    def debug(self, text):
        self.add_line(text, LogSeverity.DEBUG)

    def error(self, text):
        self.add_line(text, LogSeverity.ERROR)

    def text(self, text):
        self.add_line(text)

    def add_line(self, text, severity=LogSeverity.INFO):
        self._create_list_for_data()
        new_line = self._make_timestamped_line(text, severity)
        self.data.extend(new_line)

        self.save()


    def set_status(self, status, extra_data=None):
        self.status = status
        self.extra_data = extra_data

        self.save()