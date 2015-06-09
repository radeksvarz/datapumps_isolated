# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from django.test import TestCase

from dataviso_sequencer.lib.register import fully_qualified_path_to_module_and_class


class RegisterTestCase(TestCase):
    def test_fully_qualified_path_to_module_and_class(self):
        module_path = 'vendor_sequences.sequences.acme'
        klass_name = 'AcmeProcessSequencee'

        fully_qualified_name = module_path + "." + klass_name

        extracted_module, extracted_klass = fully_qualified_path_to_module_and_class(fully_qualified_name)

        self.assertEqual(extracted_module, module_path)
        self.assertEqual(extracted_klass, klass_name)
