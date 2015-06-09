# -*- encoding: utf-8 -*-
# ! python2

"""
Lib common mixins.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import abc


class UniqueKeyMixin(object):
    """
    This will defined property `key` on all derived classes.
    """

    @abc.abstractproperty
    def key(self):
        raise NotImplementedError("Property `key` is not defined.")