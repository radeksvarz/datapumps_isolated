# -*- encoding: utf-8 -*-
# ! python2

"""
Base classes for sequence runners.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import abc
import os

from .lib_impl.offline_data import SequenceOfflineExecution
from .types.types import IsolationLevel
from .lib.register import SequencesRegister


class Runner(object):
    """
    Base Runner.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, sequence_key):
        super(Runner, self).__init__()

        self.sequence_to_run = SequencesRegister.sequence_factory(sequence_key)

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError("Method `run` is not implemented.")

    @abc.abstractmethod
    def run_step(self, step_name, *args, **kwargs):
        raise NotImplementedError("Method `run_step` is not implemented.")


class OfflineRunner(Runner):
    """
    Offline implementation of Runner.
    """

    def __init__(self, sequence_key, input_file=None):
        super(OfflineRunner, self).__init__(sequence_key)

        normalized_path = self.validate_file(input_file)

        self.input_file = normalized_path

    def validate_file(self, input_file):
        if input_file:
            normalized_path = os.path.normpath(input_file)

            if not os.path.isfile(normalized_path):
                raise ValueError("`%s` is not a valid file!" % normalized_path)

            return normalized_path
        else:
            return None


    def run(self, *args, **kwargs):
        """
        :param force: bool
        :raise UnknownRobotSequenceException: TODO
        """

        if self.input_file:
            sequence_execution = SequenceOfflineExecution(self.input_file)
            sequence_execution.get_logger().add_line("Data from user detected")
        else:
            sequence_execution = SequenceOfflineExecution()

        sequence_execution.get_logger().add_line("Starting sequence `%s` in `offline` mode." % self.sequence_to_run)

        self.sequence_to_run.configure(
            sequence_execution=sequence_execution,
            isolation_level=IsolationLevel.DETACHED
        )

        self.sequence_to_run.run()

    def run_step(self, step_name, *args, **kwargs):
        if self.input_file:
            sequence_execution = SequenceOfflineExecution(self.input_file)
            sequence_execution.get_logger().add_line("Data from user detected")
        else:
            sequence_execution = SequenceOfflineExecution()

        sequence_execution.get_logger().add_line("Starting sequence `%s` in `offline` mode." % self.sequence_to_run)

        self.sequence_to_run.configure(
            sequence_execution=sequence_execution,
            isolation_level=IsolationLevel.DETACHED
        )

        self.sequence_to_run.run_step(step_key=step_name)