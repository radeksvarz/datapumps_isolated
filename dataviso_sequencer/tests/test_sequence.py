# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import collections

from django.test import TestCase

from ..exceptions import UnconfiguredError
from ..lib.core import Sequence, Step
from ..lib.mocks import MockedSequenceExecution
from ..types.types import IsolationLevel


class MockedSequence(Sequence):
    uuid = "42"

    def get_flow(self):
        return [MockedStep(), MockedStep()]


class MockedStep(Step):
    def get_output(self):
        pass


class SequenceTestCase(TestCase):
    def setUp(self):
        super(SequenceTestCase, self).setUp()

        self.sequence = MockedSequence()

    def test_sequence_basic_usage(self):
        self.assertIsInstance(self.sequence.get_flow(), collections.Iterable)
        self.assertRaises(UnconfiguredError, self.sequence.run)

        self.sequence.configure(
            isolation_level=IsolationLevel.DETACHED,
            sequence_execution=MockedSequenceExecution()
        )

        self.sequence.run()
