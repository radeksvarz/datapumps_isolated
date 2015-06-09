# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import re


def fprint(line):
    regex = re.compile("\[([\w\.]+)\]\s(.+)", re.IGNORECASE | re.UNICODE)
    match = regex.match(line)

    if match:
        groups = match.groups()

        final_string = "{0: <40}{1}".format(groups[0], groups[1])
    else:
        final_string = "%s" % line

    print(final_string)
