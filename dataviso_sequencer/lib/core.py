# -*- encoding: utf-8 -*-
# ! python2

"""
Core library module.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod
import abc
import logging
import os

from django.db.models.fields.files import FieldFile
import six

from ..exceptions import UnconfiguredError
from ..lib.files import TimestampedContentFile
from ..types.types import FileLookupKeys
from ..lib import data
from ..lib.common import UniqueKeyMixin


logger = logging.getLogger(__name__)


class Step(UniqueKeyMixin):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Step, self).__init__()

        self.step_logger = None
        self.qa_logger = None
        self.storage = None
        self.historical_step_execution = None
        self.previous_step_data = None
        self.are_previous_step_data_from_user = False

        self._is_configured = False


    def configure(self, step_logger, qa_logger, storage):
        """
        :type step_logger: dataviso_sequencer.lib.data.Logger
        :type qa_logger: dataviso_sequencer.lib.data.Logger
        :type storage: dataviso_sequencer.lib.data.Storage

        :rtype: dataviso_sequencer.lib.core_sequence_structure.Step
        """

        if self._is_configured:
            raise RuntimeError("Step can be configured only once.")

        assert isinstance(step_logger, data.Logger)
        assert isinstance(qa_logger, data.Logger)
        assert isinstance(storage, data.Storage)

        self.step_logger = step_logger
        self.qa_logger = qa_logger
        self.storage = storage

        self._is_configured = True

    def run(self, previous_step_data=None, historical_step_execution=None):
        """
        Run this step.

        :type previous_step_data: dataviso_sequencer.lib.data.File, django.db.models.fields.files.FieldFile
        :type historical_step_execution: dataviso_sequencer.lib.data.StepExecution

        :rtype: None
        """

        if not self._is_configured:
            raise RuntimeError("It is not possible to run a step that is not configured. "
                               "To run this step, you must call `configure(...)` method.")

        if previous_step_data:
            try:
                if isinstance(previous_step_data, six.string_types):
                    if not os.path.isfile(previous_step_data):
                        raise RuntimeError("`{0}` is not valid file".format(previous_step_data))
                else:
                    assert isinstance(previous_step_data, (data.File, FieldFile, TimestampedContentFile, file))
            except AssertionError:
                raise RuntimeError("File of type `%s` is not supported." % type(previous_step_data))

        uploaded_previous_data = self.storage.get_file_by_key(key=FileLookupKeys.USER_UPLOADED_FILE)



        # Uploaded data = highest priority
        if uploaded_previous_data:
            try:
                self.previous_step_data = uploaded_previous_data.file
            except AttributeError:
                # "Uploadovaný" soubor může být i soubor z CLI (tedy file_path)
                self.previous_step_data = uploaded_previous_data

            self.are_previous_step_data_from_user = True
        elif previous_step_data:
            self.previous_step_data = previous_step_data
        else:
            self.previous_step_data = None

        if historical_step_execution:
            assert isinstance(historical_step_execution, data.StepExecution)
            self.historical_step_execution = historical_step_execution


    def get_previous_step_data(self):
        return self.previous_step_data


    @abstractmethod
    def get_output(self):
        """
        Get return data for next step.

        :rtype: dataviso_sequencer.lib.data.File, None
        """
        raise NotImplementedError("Method `get_output` is not implemented.")


class FriendlyNameMixin(object):
    @abc.abstractproperty
    def friendly_name(self):
        raise NotImplementedError("Property `friendly_name` is not defined.")


class FriendlyKeyMixin(object):
    @abc.abstractproperty
    def friendly_key(self):
        raise NotImplementedError("Property `friendly_key` is not defined.")


class UUIDMixin(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def uuid(self):
        raise NotImplementedError("Property `uuid` is not defined.")


class Sequence(UniqueKeyMixin, UUIDMixin, FriendlyNameMixin, FriendlyKeyMixin):
    """
    Base wrapper for sequences (collection of steps).

    .. note::

       This class is typically implemented with database, stdout or file backend.

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Sequence, self).__init__()

        self.isolation_level = None
        self.sequence_execution = None
        """:type: dataviso_sequencer.lib.data.SequenceExecution"""

        self.previous_sequence_execution = None

        self.logger = None
        self.flow = None

        self._is_configured = False


    def configure(self, isolation_level, sequence_execution, previous_sequence_execution=None):
        """
        Pre-run sequence configuration.

        :param isolation_level: Are historical data accessible?
        :type isolation_level: str or unicode_literals

        :param sequence_execution: „Context“ that will be used to store log, QA and data.
        :type sequence_execution: dataviso_sequencer.lib.data.SequenceExecution

        :param previous_sequence_execution: Historical data (if available).
        :type previous_sequence_execution: :class:`dataviso_sequencer.lib.data.Logger` or None

        :raises: :class:`AssertionError` when param `sequence_execution` is not type
                    of `SequenceExecution` or when param `previous_sequence_execution`
                    is not type of `SequenceExecution`.

        :returns: Configured sequence.
        :rtype: dataviso_sequencer.lib.core.Step
        """

        assert isinstance(sequence_execution, data.SequenceExecution)

        if previous_sequence_execution:
            assert isinstance(previous_sequence_execution, data.SequenceExecution)

        self.isolation_level = isolation_level
        self.sequence_execution = sequence_execution
        self.previous_sequence_execution = previous_sequence_execution

        self.logger = self.sequence_execution.get_logger()

        self._is_configured = True

        self.set_flow()

        return self


    def check_is_configured(self, raise_ex=True):
        """
        Is sequence configured and ready to run?

        :param raise_ex: If `True` and if sequence is unconfigured, UnconfiguredError will be raised.
        :type raise_ex: bool

        :returns: True if sequence is configured.
        :rtype: bool

        :raises dataviso_sequencer.exceptions.UnconfiguredError: if sequence is not configured.
        """
        if self._is_configured:
            return True
        else:
            if raise_ex:
                raise UnconfiguredError("This sequence is *NOT* configured. Some methods are unavailable. "
                                        "Call `configure(...)` method to configure this sequence or use custom logic.")
            else:
                return False

    def run(self):
        """
        Run this sequence. The sequence must be configured – this is checked before run.

        """
        self.check_is_configured()

    def run_step(self, step_key):
        """
        Run only one step in sequence by step_key.

        :param step_key: Step key to run.
        :type step_key: str unicode_literals
        """
        self.check_is_configured()

    def set_flow(self):
        """
        Get user-defined flow and set it. This method cannot be called more than once (in one run).

        """
        self.check_is_configured()

        if not self.flow:
            self.flow = self.get_flow()
        else:
            logger.warning("Method `set_flow` called more than once.")

    def filter_flow_by_step(self, step_key):
        """
        Filter flow by given step_key.

        :param step_key: filter by this key.
        :raises Exception: step can not be found.
        """
        self.check_is_configured()

        try:
            filtered_flow = [filter(lambda one_step_in_flow: one_step_in_flow.key == step_key, self.flow)[0]]
        except IndexError:
            # TODO Raise StepNotFoundError(...)
            raise Exception("Step key \"{0}\" was not found in \"{1}\"".format(step_key, self.flow))

        self.flow = filtered_flow

    @abstractmethod
    def get_flow(self):
        """
        Simple flow getter.

        :rtype: [dataviso_sequencer.lib.core.Step]
        """
        raise NotImplementedError("Method `get_flow` is not implemented.")

    def get_sequence_execution(self):
        """
        Simple sequence execution getter. This method will check if sequence is configured.

        :rtype: dataviso_sequencer.lib.data.SequenceExecution
        """

        self.check_is_configured()

        return self.sequence_execution