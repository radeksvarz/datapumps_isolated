# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os
import sys

dirname__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dirname__)
sys.path.insert(0, os.path.join(dirname__, "../"))

from vendor_sequences.acme import AcmeSequence


SEQUENCE_REGISTER = (
    AcmeSequence,
)


def main():
    for sequence in SEQUENCE_REGISTER:
        print("Starting: ", sequence)
        sequence().run()


if __name__ == "__main__":
    main()