# -*- encoding: utf-8 -*-
# ! python2

"""
Core library module.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod


class Step(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Step, self).__init__()

        self.step_logger = None
        self.qa_logger = None
        self.storage = None

    def configure(self, step_logger, qa_logger, storage):
        """
        :type step_logger: process.lib.core_structure.Logger
        :type qa_logger: process.lib.core_structure.Logger
        :type storage: process.lib.core_structure.Storage

        :rtype: process.lib.core_sequence_structure.Step
        """
        self.step_logger = step_logger
        self.qa_logger = qa_logger
        self.storage = storage

    @abstractmethod
    def run(self, previous_step_data=None, historical_step_execution=None):
        """
        Run this step.
        """

    @abstractmethod
    def get_output(self):
        """
        Get data for next step.
        """


class Sequence(object):
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
        self.previous_sequence_execution = None

    def configure(self, isolation_level, sequence_execution, previous_sequence_execution=None):
        self.isolation_level = isolation_level
        self.sequence_execution = sequence_execution
        self.previous_sequence_execution = previous_sequence_execution

    @abstractmethod
    def get_flow(self):
        """
        Return steps.
        """

    @abstractmethod
    def run(self):
        """
        Run sequence.
        """

    @abstractmethod
    def run_step(self, step_key):
        """
        Run one step of sequence.
        """
