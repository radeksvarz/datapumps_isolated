# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from ..lib.data import SequenceExecution, Logger


class MockedSequenceExecution(SequenceExecution):
    def get_step_execution(self, key=None):
        raise NotImplementedError()

    def get_logger(self):
        return MockedLogger()


class MockedLogger(Logger):
    pass

