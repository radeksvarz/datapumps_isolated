# -*- encoding: utf-8 -*-
# ! python2

"""
Misc functions.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import random
import string

import arrow
from arrow import Arrow
import dateutil.parser
import tldextract


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    ''.join(random.SystemRandom().choice(chars) for _ in xrange(size))


def sizeof_readable(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def str_to_arrow(str_datetime, return_iso=False):
    """
    Convert **almost** any date(time)-like string to Arrow.

    Usage:

        >>> str_to_arrow("1.4.2015")
        <Arrow [2015-01-04T00:00:00+00:00]>

    :param str_datetime: Date(time)-like string.
    :param return_iso: If True and if is conversion successful, ISO format of date(time) will be returned.

    :return: Arrow object
    :rtype: arrow.Arrow
    """
    parsed_date = dateutil.parser.parse(str_datetime)
    arrow_normalized_date = arrow.get(parsed_date)

    if return_iso:
        return arrow_normalized_date.isoformat()
    else:
        return arrow_normalized_date


def get_tld(urls):
    ext = tldextract.extract(urls)

    return ext.registered_domain
