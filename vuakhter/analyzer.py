from __future__ import annotations
import typing

from vuakhter.utils.helpers import timestamp

if typing.TYPE_CHECKING:
    from vuakhter.base.access_log import AccessLog
    from vuakhter.metrics.base import StatisticsMetrics
    from vuakhter.utils.types import DateOrDatetime

    MetricsIterable = typing.Iterable[StatisticsMetrics]
    MetricsList = typing.List[StatisticsMetrics]
    PrefixesIterable = typing.Iterable[str]


class HttpAnalyzer:
    def __init__(
            self, access_log: AccessLog,
            prefixes: PrefixesIterable = None,
            metrics: MetricsIterable = None,
    ) -> None:
        self.access_log = access_log
        self.prefixes = list(prefixes or ['/'])
        self._metrics = list(metrics or [])

    @property
    def metrics(self) -> MetricsList:
        return self._metrics

    def add_metric(self, metric: StatisticsMetrics) -> None:
        self._metrics.append(metric)

    def analyze(self, start_date: DateOrDatetime, end_date: DateOrDatetime) -> None:
        if not self._metrics:
            return

        start_ts = timestamp(start_date, ms=True)
        end_ts = timestamp(end_date, ms=True)

        for metric in self._metrics:
            metric.initialize()

        for entry in self.access_log.get_records(start_ts, end_ts, prefixes=self.prefixes):
            for metric in self._metrics:
                metric.process_entry(entry)
