# -*- encoding: utf-8 -*-
# ! python2

"""
Django application configuration introduced in `1.7`.
For more info see: https://docs.djangoproject.com/en/1.7/ref/applications/#application-configuration.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from django.apps import AppConfig


class DatavisoSequencerAppConfig(AppConfig):
    """
    Django app config, this will set human readable name in Django admin.
    """

    name = 'dataviso_sequencer'
    verbose_name = "Dataviso Sequencer"

    def ready(self):
        # noinspection PyUnresolvedReferences
        pass