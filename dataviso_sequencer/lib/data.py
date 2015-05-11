# -*- encoding: utf-8 -*-
# ! python2

"""
All data base classes.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import abc

from ..types.types import LogSeverity


class File(object):
    """
    File created during:

        - step execution;
        - user upload.
    """

    @abc.abstractmethod
    def get_file(self):
        """
        Get real Python file.

        :rtype: django.core.files.File
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_file_name(self):
        """
        Get real Python file.

        :rtype: django.core.files.File
        """
        raise NotImplementedError("Method `get_file_name` is not implemented.")

    @abc.abstractmethod
    def check_file(self):
        """
        Check if file exists.

        :rtype: bool
        """
        raise NotImplementedError("Method `check_file` is not implemented.")


class Storage(object):
    """
    Storage for files.
    """
    __metaclass__ = abc.ABCMeta

    def add_file(self, file_obj, file_category, key=None):
        """
        :rtype: process.lib.core_structure.File
        """
        if not file_obj:
            raise ValueError("When adding file, parameter `file_obj` cannot be None.")

    @abc.abstractmethod
    def add_internal_file(self, file_obj, file_category, key=None):
        """
        :rtype: process.lib.core_structure.File
        """
        raise NotImplementedError("Method `add_internal_file` is not implemented.")

    @abc.abstractmethod
    def get_file_by_key(self, key):
        """
        :rtype: process.lib.core_structure.File
        """
        raise NotImplementedError("Method `get_file_by_key` is not implemented.")

    @abc.abstractmethod
    def get_all_files(self):
        """
        :rtype: process.lib.core_structure.File
        """
        raise NotImplementedError("Method `get_all_files` is not implemented.")


class LoggableProcessItem(object):
    """
    Define `get_logger` on all derived classes.
    """

    @abc.abstractmethod
    def get_logger(self):
        """
        Logger getter.

        :return: Item logger
        :rtype: dataviso_sequencer.lib.data.Logger
        """
        raise NotImplementedError("Method `get_logger` is not implemented.")


class StatusItem(object):
    """
    Define `set_status` on all derived classes.
    """

    @abc.abstractmethod
    def set_status(self, status, extra_data=None):
        """
        Status setter

        :param status: Status to set.
        :type status: str or unicode_literals

        :param extra_data: Some extra data (e.g. exception message)
        :type extra_data: str or unicode_literals

        :rtype: None
        """
        raise NotImplementedError("Method `set_status` is not implemented.")


class SequenceExecution(LoggableProcessItem, StatusItem):
    """
    Execution of a sequence.
    """

    @abc.abstractmethod
    def get_step_execution(self, key):
        """
        :type key: str, unicode_literals
        :rtype: process.lib.core_structure.StepExecution
        """
        raise NotImplementedError("Method `get_step_execution` is not implemented.")


class StepExecution(LoggableProcessItem, StatusItem):
    """
    Execution of a step.
    """

    @abc.abstractmethod
    def get_storage(self):
        """
        :rtype: process.lib.core_structure.Storage
        """
        raise NotImplementedError("Method `get_storage` is not implemented.")

    @abc.abstractmethod
    def get_qa_logger(self):
        """
        :rtype: process.lib.core_structure.Logger
        """
        raise NotImplementedError("Method `get_qa_logger` is not implemented.")


class Logger(object):
    """
    Every :class:`SequenceExecution` and :class:`StepExecution` has its own Logger.
    """

    def add_text(self, text):
        """
        Add multiple lines of text.

        :param text: Text to add
        :type text: str or unicode_literals

        :rtype: None
        """
        pass

    def add_line(self, line, severity=LogSeverity.INFO):
        """
        Add single line of text.

        :param line: Text to add
        :type line: str or unicode_literals

        :rtype: None
        """
        pass

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

    @abc.abstractmethod
    def save(self, *args, **kwargs):
        """
        Save current logger session. Defined here for compatibility with Django model.
        """
        pass
