# -*- encoding: utf-8 -*-
# ! python2

"""
Extractors base class.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod
import json

from ..lib.core import Step


class Extractor(Step):
    __metaclass__ = ABCMeta
    key = "extractor"

    def __init__(self):
        super(Extractor, self).__init__()

    @abstractmethod
    def get_output(self):
        raise NotImplementedError()

    def txt_to_json(self, txt):
        """
        Convert text to JSON.

        :param txt: Text to convert
        :return: JSON
        """
        raw_data = json.loads(txt)
        pretty_data = json.dumps(raw_data, indent=4, sort_keys=True)

        return pretty_data
