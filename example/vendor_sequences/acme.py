# -*- encoding: utf-8 -*-
# ! python2

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import requests

from dataviso_sequencer.lib.core import Step, Sequence
from dataviso_sequencer.types.types import StepStateControlCodes


class AcmeTracker(Step):
    def run(self, previous_step_data=None, **kwargs):
        r = requests.get('http://www.example.com')

        if r.headers["last-modified"] != "previous tracking date":
            status_text_continue = "continue to downloader"
            return StepStateControlCodes.CONTINUE, status_text_continue
        else:
            status_text_exit = "no new data"
            return StepStateControlCodes.EXIT, status_text_exit


    def get_output(self):
        pass


class AcmeDownloader(Step):
    def __init__(self):
        super(AcmeDownloader, self).__init__()

        self.output = None

    def run(self, previous_step_data=None, historical_step_execution=None):
        r = requests.get('http://www.example.com')
        data_to_store = r.text

        with open('stored_example_com.html', 'a') as the_file:
            the_file.write(data_to_store)

        self.output = data_to_store

    def get_output(self):
        return self.output


class AcmeSequence(Sequence):
    def __init__(self):
        super(AcmeSequence, self).__init__()

    def get_flow(self):
        return [AcmeTracker(), AcmeDownloader()]


    def run(self):
        previous_data = None

        for step in self.get_flow():
            this_data = step.run(previous_step_data=previous_data)

            previous_data = this_data

    def run_step(self, step_key):
        raise NotImplementedError()