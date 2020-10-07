from __future__ import annotations

import collections
import typing
import math

from vuakhter.metrics.base import StatisticsMetrics
from vuakhter.utils.helpers import get_endpoint, is_valid
from vuakhter.utils.types import TimestampRange

if typing.TYPE_CHECKING:
    from vuakhter.base.requests_log import RequestsLog
    from vuakhter.utils.types import AccessEntry
    from vuakhter.metrics.base import StatisticsMapping


class MethodCounter(StatisticsMetrics):
    description = 'Response counts by method'

    def process_entry(self, entry: AccessEntry) -> None:
        self._statistics[entry.method] += 1


class EndpointCounter(StatisticsMetrics):
    description = 'Response counts by endpoint'

    def process_entry(self, entry: AccessEntry) -> None:
        endpoint = get_endpoint(entry.url)
        self._statistics[endpoint] += 1


class StatusCounter(StatisticsMetrics):
    description = 'Response counts by status'

    def process_entry(self, entry: AccessEntry) -> None:
        self._statistics[entry.status_code] += 1


class ComplexCounter(StatisticsMetrics):
    description = 'Response counts by endpoint, method, status'

    def process_entry(self, entry: AccessEntry) -> None:
        key = (get_endpoint(entry.url), entry.method, entry.status_code)
        self._statistics[key] += 1


class ResponseTimeCounter(StatisticsMetrics):
    description_prefix = 'Response counts by time took'

    def __init__(self, fraction: float = 0.50):
        super().__init__()
        self.fraction = fraction

    @property
    def description(self) -> typing.Any:
        return f'{self.description_prefix} fraction by {self.fraction} ms'

    def process_entry(self, entry: AccessEntry) -> None:
        response_time = math.ceil(entry.response_time / self.fraction) * self.fraction
        self._statistics[response_time] += 1


class SlowLogCounter(StatisticsMetrics):
    description = 'Top endpoints response time'

    def __init__(self, top: int = 10, mangle: bool = True) -> None:
        self.top = top
        self.mangle = mangle

    def initialize(self) -> None:
        self._statistics: StatisticsMapping = collections.defaultdict(list)

    def process_entry(self, entry: AccessEntry) -> None:
        endpoint = get_endpoint(entry.url) if self.mangle else entry.url

        top_list = self._statistics['top']

        top_list.append((endpoint, entry.response_time))

        if len(top_list) > self.top * 100:
            self._statistics['top'] = sorted(top_list, key=lambda a: a[1], reverse=True)[0:self.top]

    def finalize(self) -> None:
        top_list = self._statistics['top']
        self._statistics['top'] = sorted(top_list, key=lambda a: a[1], reverse=True)[0:self.top]

    def report(self) -> str:
        return '\n'.join((f'{endpoint} {rtime}' for endpoint, rtime in self._statistics['top']))


class SchemaValidatorCounter(StatisticsMetrics):
    description = 'Number of valid with schema responses'

    def __init__(self, requests_log: RequestsLog):
        super().__init__()
        self.requests_log = requests_log
        self.min_ts = 0
        self.max_ts = 0
        self.check_ids: typing.List[str] = []

    def process_buffer(self) -> None:
        if not self.check_ids:
            return
        valid_cnt, invalid_cnt = 0, 0
        for record in self.requests_log.get_records(
            TimestampRange(self.min_ts, self.max_ts),
            request_ids=self.check_ids,
        ):
            if is_valid(record):
                valid_cnt += 1
            else:
                invalid_cnt += 1

        self._statistics['valid'] += valid_cnt
        self._statistics['invalid'] += invalid_cnt
        self._statistics['missed'] += len(self.check_ids) - (valid_cnt + invalid_cnt)

        self.min_ts = 0
        self.max_ts = 0
        self.check_ids = []

    def process_entry(self, entry: AccessEntry) -> None:
        if entry.method == 'OPTIONS':
            return
        if not self.min_ts or entry.ts < self.min_ts:
            self.min_ts = entry.ts
        if not self.max_ts or entry.ts > self.max_ts:
            self.max_ts = entry.ts
        self.check_ids.append(entry.request_id)
        if len(self.check_ids) >= 100:
            self.process_buffer()

    def finalize(self) -> None:
        self.process_buffer()

    def report(self) -> str:
        valid, invalid, missed = self._statistics['valid'], self._statistics['invalid'], self._statistics['missed']
        validated = (valid + invalid)
        rate = 0.0
        if validated:
            rate = 100.0 * self._statistics['valid'] / validated
        return f'Valid requests {rate:.2f}% ({valid} out of {validated}, {missed} missed)'
