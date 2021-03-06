# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta

from ..exceptions import UseAsEnumOnlyException


class Enum(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        raise UseAsEnumOnlyException("It is not possible to call `__init__` on Enum.")