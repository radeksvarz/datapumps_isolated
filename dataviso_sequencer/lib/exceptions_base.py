# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import abc


class BaseSequencerException(Exception):
    __metaclass__ = abc.ABCMeta


class StepFlowException(BaseSequencerException):
    reason = None

    def __init__(self, *args, **kwargs):
        reason = kwargs.pop('reason', None)

        if not self.reason and reason:
            self.reason = reason

        super(StepFlowException, self).__init__(*args, **kwargs)