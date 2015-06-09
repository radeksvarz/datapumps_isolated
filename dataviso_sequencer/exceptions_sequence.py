# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from .lib.exceptions_base import StepFlowException


class SourceCodeChangedError(StepFlowException):
    pass


class HaltStepException(StepFlowException):
    pass


class InvalidReturnedStatusError(HaltStepException):
    pass


class UnknownReturnedStatusError(HaltStepException):
    pass


class ExitStepException(StepFlowException):
    pass


class NotImplemenetedStepError(HaltStepException):
    code = 501
    reason = "Not implemented"


class DownloaderError(HaltStepException):
    code = 502


class NotModifiedError(ExitStepException):
    code = 500


class FileMismatchEror(HaltStepException):
    code = 500
    reason = "Input file mismatch"


class UnknownRobotSequenceException(Exception):
    pass


class StepLoggerDoesNotExistException(Exception):
    pass


class UnexpectedStructureError(HaltStepException):
    reason = "Unexpected structure"


class SourceStructureError(HaltStepException):
    reason = "Source structure error"


class CorruptedFileError(HaltStepException):
    code = 503
    reason = "Corrupted file"


class NonePreviousStepDataError(HaltStepException):
    code = 502
    reason = "No previous data"


class OutputValidationError(HaltStepException):
    pass
