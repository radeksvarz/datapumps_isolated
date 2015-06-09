# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import warnings

from ..lib_impl.offline_utils import fprint

from ..types.types import LogSeverity, FileLookupKeys
from ..lib.data import Logger, Storage, StepExecution, SequenceExecution
from ..lib.mixins import DummyStatusItem


class OfflineLogger(Logger):
    def add_text(self, text):
        self.add_line(text)

    def add_line(self, line, severity=LogSeverity.INFO):
        fprint("[OfflineLogger.add_line] %s" % line)


class OfflineStorage(Storage):
    def __init__(self, input_file):
        super(OfflineStorage, self).__init__()

        self.input_file = input_file

    def get_file_by_key(self, key):
        if key == FileLookupKeys.USER_UPLOADED_FILE and self.input_file:
            # Step se snaží získat data uploadovaná uživatelem
            # my máme data z CLI (přepínač --file=...), dáme mu tedy data z CLI (v CLI nedává upload smysl)
            fprint("[OfflineStorage.get_file_by_key] Returning %s" % self.input_file)
            return self.input_file
        else:
            warnings.warn(
                "It is not possible to get file in offline mode. "
                "*NOT* Returning file with key `%s`." % key,
                RuntimeWarning
            )

        return None

    def add_file(self, file_obj, file_category, key=None):
        fprint("[OfflineStorage.add_file] Adding file `%s`" % file_obj)

        return file_obj

    def add_internal_file(self, file_obj, file_category, key=None):
        return self.add_file(file_obj, file_category, key)

    def get_all_files(self):
        if self.input_file:
            return [self.input_file]
        else:
            fprint("[OfflineStorage.get_all_files] Offline mode does not store any data, method will return [].")

            return []


class OfflineStepExecution(StepExecution, DummyStatusItem):
    def __init__(self, input_file):
        super(OfflineStepExecution, self).__init__()

        self._logger = OfflineLogger()
        self._offline_storage = OfflineStorage(input_file)

    def get_logger(self):
        return self._logger

    def get_qa_logger(self):
        return self._logger

    def get_storage(self):
        return self._offline_storage


class SequenceOfflineExecution(SequenceExecution, DummyStatusItem):
    def __init__(self, input_file=None):
        super(SequenceOfflineExecution, self).__init__()

        self._logger = OfflineLogger()
        self._step_execution = {}
        self.input_file = input_file

    def get_logger(self):
        return self._logger

    def get_step_execution(self, key):
        if key not in self._step_execution:
            self._step_execution[key] = OfflineStepExecution(self.input_file)

        return self._step_execution[key]