# -*- encoding: utf-8 -*-
# ! python2

"""
Trackers base class.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from abc import ABCMeta
import json

from django.utils.text import slugify
import requests

from dataviso_sequencer.funcs import get_tld
from ..exceptions_sequence import DownloaderError
from ..lib.files import TimestampedContentFile
from ..types.types import FileExtensions, StepStateControlCodes, SuccessControlReason, \
    FileLookupKeys, FileCategories
from ..exceptions import UnconfiguredError
from ..exceptions_sequence import FileMismatchEror
from ..lib.core import Step
from ..types.types import RemoteSourceState


class Tracker(Step):
    __metaclass__ = ABCMeta
    key = "tracker"

    def run(self, previous_step_data=None, historical_step_execution=None):
        if previous_step_data:
            raise FileMismatchEror("Tracker with input data (`%s`) does not make sense." % previous_step_data)

        if len(self.storage.get_all_files()) > 0:
            raise FileMismatchEror(
                "Tracker with input data (`%s`) in storage does not make sense." % self.storage.get_all_files())

        super(Tracker, self).run(previous_step_data, historical_step_execution)


class URLHeadersTracker(Tracker):
    """
    Base Tracker class. This class fetches specified headers and compares with previous data.
    """

    header_to_compare = None
    """Name of single header to compare"""

    tracking_url = None
    """Location to check"""

    key = "tracker"
    """Unique key because tracker is also step"""

    available_methods = ["HEAD", "GET"]

    def __init__(self):
        super(URLHeadersTracker, self).__init__()

        if not self.tracking_url:
            raise UnconfiguredError("Tracking URL is not set.")

        # Convert single URL to iterable
        # This will fail on strings, see: http://stackoverflow.com/a/1952481/752142
        if not hasattr(self.tracking_url, '__iter__'):
            self.tracking_url = [self.tracking_url]

        self.remote_headers = {}
        self.prev_header_file = None

    def fetch_remote_header(self, url):
        """
        Make `HTTP GET` request and retrieve header specified in `self.header_to_compare`.

        :return: Remote header
        """
        self.step_logger.add_line("Checking URL '{0}'.".format(url))

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        head_response = {}

        for method in self.available_methods:
            if method == "HEAD":
                head_response = requests.head(url, headers=headers, allow_redirects=True, verify=True)
            elif method == "GET":
                head_response = requests.get(url, headers=headers, allow_redirects=True, verify=True)
            else:
                raise ValueError("HTTP method `{0}` is not supported.".format(method))

            if self.header_to_compare not in head_response.headers:
                self.step_logger.warning("`{0}` is not in {1}, trying next.".format(self.header_to_compare, method))
                continue
            else:
                self.step_logger.info("Successfully fetched {0} from {1}".format(self.header_to_compare, method))
                break

        remote_header = head_response.headers[self.header_to_compare]

        # print("{0} = {1}".format(self.header_to_compare, remote_header))

        self.step_logger.add_line("Fetched remote header: '{0}'.".format(remote_header))

        return remote_header

    def try_clean(self, remote_header):
        """
        Derived class can have method `clean_{name_of_header_to_compare}`.

        Full example:

        ::

            class ExampleTracker(URLHeadersTracker):
                self.header_to_compare = "last-modified"

                def clean_last_modified(value):
                    return value.lower()

        :param remote_header: Remote header to clean
        :type remote_header: str or unicode_literals

        :return: Possibly cleaned header
        :rtype: str or unicode_literals
        """
        clean_method_name = "clean_{0}".format(slugify(self.header_to_compare).replace("-", "_"))

        try:
            clean_method = getattr(self, clean_method_name)
        except AttributeError:
            # No such method, clean_xx methods are optional
            pass
        else:
            remote_header = clean_method(remote_header)

        return remote_header

    def is_remote_source_changed(self, prev_header, url):
        """
        Make HTTP request to remote source and compare remote header with given header.

        Return code is simple boolean value. You can use as more readable version these shortcuts:

            >>> assert RemoteSourceState.CHANGED == True
            >>> assert RemoteSourceState.SAME_AS_BEFORE == False

        :param prev_header: str or unicode_literals
        :return: True if source is different, False if source is same as before
        :rtype: bool
        """

        # Make HTTP request
        remote_header = self.fetch_remote_header(url)
        self.remote_headers[url] = remote_header = self.try_clean(remote_header)

        if not prev_header:
            # No previous header, we have nothing to compare
            # == e.g. first run => always changed
            return RemoteSourceState.CHANGED

        prev_header = self.try_clean(prev_header)

        if remote_header != prev_header:
            return RemoteSourceState.CHANGED
        else:
            return RemoteSourceState.SAME_AS_BEFORE

    def run(self, previous_step_data=None, historical_step_execution=None):
        super(URLHeadersTracker, self).run(previous_step_data, historical_step_execution)

        self.step_logger.add_line(
            "Tracker started with "
            "historical data: {0}".format(str(historical_step_execution))
        )

        self.set_previous_header_file()

        try:
            source_state = self.check_source_changed()
            self.step_logger.add_line("Checking remote source finished")
        except (requests.ConnectionError, KeyError) as e:
            raise DownloaderError(e)

        if RemoteSourceState.CHANGED == source_state:
            return StepStateControlCodes.CONTINUE, SuccessControlReason.SOURCE_CHANGED
        else:
            return StepStateControlCodes.EXIT, SuccessControlReason.NOT_MODIFIED

    def set_previous_header_file(self):
        try:
            historic_data = self.historical_step_execution.get_historical_data(key=FileLookupKeys.HEADER_FILE)

            self.prev_header_file = historic_data[0]

            self.storage.add_internal_file(self.prev_header_file, FileCategories.INPUT)
            self.step_logger.add_line("Historical data from previous run: %s" % self.prev_header_file.get_file_name())
        except (IndexError, AttributeError):
            self.prev_header_file = None
            self.step_logger.warning("No historical data")

    def get_all_previous_headers(self):
        if not self.prev_header_file:
            return None

        try:
            with open(self.prev_header_file.get_file_name()) as content_file:
                previous_header = json.load(content_file)
        except IOError as e:
            self.step_logger.error(e)
            return None

        return previous_header

    def save_remote_headers_to_file(self, remote_headers):
        data = json.dumps(remote_headers, indent=4)

        filename = "remote_headers_" + get_tld(self.tracking_url[0])
        new_content_file = TimestampedContentFile(data, name=filename, extension=FileExtensions.JSON)

        self.storage.add_internal_file(new_content_file, FileCategories.OUTPUT, FileLookupKeys.HEADER_FILE)

    def check_source_changed(self):
        """
        Compare all previous headers with real headers. One changed URL means changed source.

        :return: True if any of url is changed.
        """
        previous_header = self.get_all_previous_headers()

        previous_header = previous_header if previous_header else {}
        any_url_changed = False

        for url in self.tracking_url:
            if url in previous_header:
                prev_header_for_url = previous_header[url]
            else:
                # Maybe this is new URL or first run
                prev_header_for_url = None

            self.step_logger.add_line("Last-modified for `{0}` from file: {1}".format(url, prev_header_for_url))
            remote_state = self.is_remote_source_changed(prev_header_for_url, url)

            if remote_state == RemoteSourceState.CHANGED:
                self.step_logger.warning("Remote state of URL `{0}` is changed.".format(url))
                # Method will return CHANGED, but do not return here! We need data for all urls.
                any_url_changed = True

        self.save_remote_headers_to_file(self.remote_headers)

        if any_url_changed:
            return RemoteSourceState.CHANGED
        else:
            return RemoteSourceState.SAME_AS_BEFORE
