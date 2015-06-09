# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from .enum import Enum


class StepStateControlCodes(Enum):
    _halt = "halted"
    _programmatic_error = "programmatic_error"

    EXIT = "finished"
    CONTINUE = "continue"
    WAITING_INPUT_FILE = "waiting_input_file"

    # Ke stavu UNKNOWN musí být přiřazeno None !
    # Funkce, která v Pythonu nic nevrátí, vrátí None... pokud tedy
    # programátor v kroku zapomene vrátit stav, poznáme
    UNKNOWN = None

    @staticmethod
    def validate_status(status):
        # TODO Napsat hezčí
        valid_statuses = [
            StepStateControlCodes.CONTINUE, StepStateControlCodes.EXIT,
            StepStateControlCodes.WAITING_INPUT_FILE
        ]

        if status not in valid_statuses:
            return False
        else:
            return True


class SuccessControlReason(Enum):
    DOWNLOADED = "200, Data downloaded"
    SOURCE_CHANGED = "42, Source changed"
    EXTRACTED = "42, Extracted"
    NORMALIZED = "42, Normalized"
    NOT_MODIFIED = "304, Not modified"
    WAITING_FOR_USER = "42, Waiting for user"
    IMPORTED = "42, Imported"
    UPLOADED = "42, Uploaded"


class ErrorControlReason(Enum):
    NOT_IMPLEMENTED = "500, Not implemented"

class RunMode(Enum):
    NORMAL = "normal"
    FORCE = "force"


class IsolationLevel(Enum):
    DETACHED = "detached"
    HISTORY_ENABLED = "history_enabled"


class RemoteSourceState(Enum):
    CHANGED = True
    SAME_AS_BEFORE = False


class FileLookupKeys(Enum):
    HEADER_FILE = "header"
    USER_UPLOADED_FILE = "user_uploaded_file"


class FileExtensions(Enum):
    JSON = "json"
    HTML = "html"
    TSV = "tsv"
    CSV = "csv"


class NamedStrings(Enum):
    EMPTY_STR = ""


class RunTypes(Enum):
    CLI = "cli"
    AUTORUN = "autorun"
    MANUAL = "manual"
    DEBUG_MODE = "debug_mode"


class FileCategories(Enum):
    OUTPUT = "output"
    INPUT = "input"


class AutorunFrequencies(Enum):
    EVERY_MINUTE = "every_minute"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class LogSeverity(Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4