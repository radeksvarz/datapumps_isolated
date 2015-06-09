# -*- encoding: utf-8 -*-
# ! python2

"""
Importers base class.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

from ..lib.core import Step


class Importer(Step):
    __metaclass__ = ABCMeta

    @property
    def key(self):
        return "importer"

    def __init__(self):
        super(Importer, self).__init__()

    @abstractmethod
    def get_output(self):
        raise NotImplementedError()