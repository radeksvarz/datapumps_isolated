# -*- encoding: utf-8 -*-
# ! python2

"""
All exceptions used in the Dataviso sequencer code base are defined here.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from .lib.exceptions_base import BaseSequencerException


class UseAsEnumOnlyException(BaseSequencerException):
    pass


class StepException(BaseSequencerException):
    pass


class UnknownStepStatusException(StepException):
    pass


class InvalidStepStatusException(StepException):
    pass


class SequenceException(BaseSequencerException):
    pass


class SequenceProcessHaltedException(SequenceException):
    pass


class SequenceExitException(SequenceException):
    pass


class UnconfiguredError(BaseSequencerException):
    pass