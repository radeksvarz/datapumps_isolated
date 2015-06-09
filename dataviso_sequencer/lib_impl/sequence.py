# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta
import logging
import traceback

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from ..exceptions_sequence import SourceCodeChangedError, InvalidReturnedStatusError, \
    HaltStepException
from ..lib.core import Sequence
from ..types.types import IsolationLevel, StepStateControlCodes
from ..lib.mixins import FakeFlowMixin


logger = logging.getLogger(__name__)


class LinearProcessSequence(Sequence, FakeFlowMixin):
    __metaclass__ = ABCMeta
    key = "linear_sequence"

    def __init__(self):
        super(LinearProcessSequence, self).__init__()

        self.sequence_logger = None


    def is_history_available(self):
        return self.previous_sequence_execution and self.isolation_level == IsolationLevel.HISTORY_ENABLED

    def validate_previous_steps(self, previous_steps):
        prev_count = previous_steps.count()
        current_count = len(self.flow)

        self.sequence_execution.debug(
            "Count of previous steps: %s; Count of steps in this execution: %s" % (prev_count, current_count)
        )

        return prev_count == current_count


    def get_previous_steps(self):
        return self.previous_sequence_execution.stepexecution_set.all()

    def prepare_previous_steps(self):
        if self.is_history_available():
            previous_steps = self.get_previous_steps()

            if not self.validate_previous_steps(previous_steps):
                self.sequence_logger.warning("This and previous sequence is different. "
                                             "Unable to map step on step.")
            else:
                return previous_steps

        return self.generate_fake_flow(self.flow)

    def reraise_if_debug(self, status):
        if (
                status == StepStateControlCodes._programmatic_error or status == StepStateControlCodes._halt) and not settings.SURPRESS_EXCEPTIONS:
            # Raise latest raised exception
            raise

    def get_step_execution_by_key(self, step):
        try:
            step_execution = self.sequence_execution.get_step_execution(key=step.key)
        except ObjectDoesNotExist as e:
            raise SourceCodeChangedError("Source code has changed since this run. "
                                         "Cannot restore execution.")
        return step_execution

    def run(self):
        super(LinearProcessSequence, self).run()

        data_for_next_step = reason = None

        self.sequence_logger = self.sequence_execution.get_logger()
        self.sequence_logger.add_line("Base sequence started")

        previous_steps = self.prepare_previous_steps()

        step_counter = 0

        for step in self.flow:

            # TODO Použít trik: https://github.com/brennerm/PyTricks/blob/master/tryelse.py

            self.sequence_logger.add_line("Starting step '{0}'.".format(step.key))

            step_execution = self.get_step_execution_by_key(step)

            step_status = StepStateControlCodes.UNKNOWN
            prev_step = previous_steps[step_counter]

            if prev_step:
                prev_step.mark_historical()

            step.configure(
                step_logger=step_execution.get_logger(),
                qa_logger=step_execution.get_qa_logger(),
                storage=step_execution.get_storage()
            )

            try:
                result = step.run(
                    previous_step_data=data_for_next_step,
                    historical_step_execution=prev_step
                )

                reason = "Unknown reason"

                try:
                    step_status, reason = result
                except TypeError:
                    raise TypeError("Method `run` on step must return tuple or raise Exception.")

                if not StepStateControlCodes.validate_status(step_status):
                    raise InvalidReturnedStatusError(reason="%s invalid" % step_status)

            except HaltStepException as ex:
                # Výjimka, kterou programátor kroku vyhodil při jemu známé situaci
                step_status = StepStateControlCodes._halt
                reason = ex.reason

                self.sequence_logger.warning("Step was halted by programmer from step catched: %s" % ex)

                if not settings.LOG_SEQUENCE_EXCEPTIONS:
                    logger.warning(ex, extra={'step': step, 'stack': True})

            except Exception as ex:
                step_status = StepStateControlCodes._programmatic_error
                reason = ex

                if not settings.LOG_SEQUENCE_EXCEPTIONS:
                    logger.error(ex, extra={'step': step, 'stack': True})

            finally:
                step_execution.set_status(step_status, reason)

                # Always save latest step status as sequence status
                self.sequence_execution.set_status(step_status, reason)

                if step_status != StepStateControlCodes.CONTINUE:
                    self.sequence_logger.add_line("Step finished with status %s" % step_status)
                    self.reraise_if_debug(step_status)

                    # Do not run next step
                    return

            # noinspection PyUnusedLocal
            data_for_next_step = step.get_output()

            del step_execution, reason, step_status
            step_counter += 1

    def run_step(self, step_key):
        super(LinearProcessSequence, self).run_step(step_key)

        self.filter_flow_by_step(step_key)
        self.run()