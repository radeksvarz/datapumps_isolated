# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from ..lib_impl.offline_utils import fprint

from ..lib.data import StatusItem


class DummyOutputMixin(object):
    """
    If your step has nothing to return, subclass this mixin.
    """

    def __init__(self):
        super(DummyOutputMixin, self).__init__()

    def get_output(self):
        return None


class DummyStatusItem(StatusItem):
    """
    This will print status tu stdout.
    """

    def set_status(self, status, extra_data=None):
        fprint(
            "[DummyStatusItem.set_status] "
            "Status has been set to `{0}` "
            "with extra_data `{1}`".format(status, extra_data)
        )


class FakeFlowMixin(object):
    """
    Generate fake flow from 'None'.
    """

    def generate_fake_flow(self, flow):
        return [None] * len(flow)