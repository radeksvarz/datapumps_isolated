# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from .enum import Enum


class StepStateControlCodes(object):
    EXIT = "finished"
    CONTINUE = "continue"


class LogSeverity(Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4