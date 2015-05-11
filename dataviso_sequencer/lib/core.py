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
