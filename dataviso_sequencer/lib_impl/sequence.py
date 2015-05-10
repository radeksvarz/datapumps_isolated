# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta

from ..lib.core import Sequence


class LinearProcessSequence(Sequence):
    __metaclass__ = ABCMeta
    key = "linear_sequence"

    def __init__(self):
        super(LinearProcessSequence, self).__init__()

    def run(self):
        super(LinearProcessSequence, self).run()

    def run_step(self, step_key):
        super(LinearProcessSequence, self).run_step(step_key)
