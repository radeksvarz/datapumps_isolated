# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import importlib

from django.conf import settings

from ..exceptions_sequence import UnknownRobotSequenceException


def fully_qualified_path_to_module_and_class(fully):
    splited = fully.split(".")

    klass_name = splited.pop()

    module_name = ".".join(splited)

    return module_name, klass_name


def class_from_fqpath(fully_qualified_path):
    module_name, class_name = fully_qualified_path_to_module_and_class(fully_qualified_path)

    # load the module, will raise ImportError if module cannot be loaded
    module = importlib.import_module(module_name)

    # get the class, will raise AttributeError if class cannot be found
    klass = getattr(module, class_name)

    return klass


_sequences_by_vendor_cache = {}


def refresh_sequences(override_duplicates=False):
    for fq_value in settings.AVAILABLE_SEQUENCES:
        key = class_from_fqpath(fq_value).friendly_key

        if key in _sequences_by_vendor_cache and not override_duplicates:
            raise ValueError("Item `settings.AVAILABLE_SEQUENCES` contains duplicate `friendly_key` values. "
                             "Check your sequences for duplicate `%s` value." % key)

        _sequences_by_vendor_cache[key] = class_from_fqpath(fq_value)


refresh_sequences()


class SequencesRegister(object):
    SEQUENCES_BY_VENDOR = _sequences_by_vendor_cache

    def __init__(self):
        raise RuntimeError("It is not possible to instantiate `SequencesRegister`.")

    @staticmethod
    def sequence_factory(sequence_key):
        sequence_class = SequencesRegister.get_sequence_class_by_key(sequence_key)
        sequence = sequence_class()

        return sequence

    @staticmethod
    def get_sequence_class_by_key(sequence_key):
        try:
            sequence_class = SequencesRegister.SEQUENCES_BY_VENDOR[sequence_key]
        except KeyError:
            raise UnknownRobotSequenceException("Sequence for \"{0}\" was not found".format(sequence_key))

        return sequence_class

    @staticmethod
    def get_choices():
        return [(key, klass.friendly_name) for key, klass in _sequences_by_vendor_cache.items()]