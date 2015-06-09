# -*- encoding: utf-8 -*-
# ! python2

"""
Normalizers base class.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta

from ..lib.core import Step


class Normalizer(Step):
    __metaclass__ = ABCMeta
    key = "normalizer"

    def __init__(self):
        super(Normalizer, self).__init__()