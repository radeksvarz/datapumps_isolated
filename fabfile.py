# coding=utf-8

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import sys

import six

if not six.PY2:
    print("Run Fabfile only under Python 2.x")
    sys.exit(0)

from fabric.decorators import task
from fabric.operations import local

try:
    from color_printer.colors import green, red
except ImportError:
    green = red = print


@task()
def test():
    local("nosetests --with-coverage --cover-package=dataviso_sequencer --cover-tests --cover-erase --with-doctest")

    green("Tests OK.")
