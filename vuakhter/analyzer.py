from __future__ import annotations
import typing

from vuakhter.base.base_log import BaseLog
from vuakhter.utils.types import TimestampRange

if typing.TYPE_CHECKING:
    from vuakhter.base.access_log import AccessLog
    from vuakhter.metrics.base import StatisticsMetrics
    from vuakhter.utils.types import DateOrDatetime

    MetricsIterable = typing.Iterable[StatisticsMetrics]
    MetricsList = typing.List[StatisticsMetrics]
    PrefixesIterable = typing.Iterable[str]


class BaseLogAnalyzer:
    def __init__(
        self, log: BaseLog,
        metrics: MetricsIterable = None,
    ) -> None:
        self.log = log
        self._metrics = list(metrics or [])

    @property
    def metrics(self) -> MetricsList:
        return self._metrics

    def add_metric(self, metric: StatisticsMetrics) -> None:
        self._metrics.append(metric)

    def analyze(self, start_date: DateOrDatetime, end_date: DateOrDatetime, **kwargs: typing.Any) -> None:
        if not self._metrics:
            return

        ts_range = TimestampRange.from_datetime(start_date, end_date, ms=True)

        for metric in self._metrics:
            metric.initialize()

        for entry in self.log.get_records(ts_range, **kwargs):
            for metric in self._metrics:
                metric.process_entry(entry)


class AccessLogAnalyzer(BaseLogAnalyzer):
    def __init__(
        self, access_log: AccessLog,
        metrics: MetricsIterable = None,
    ) -> None:
        super().__init__(access_log, metrics)
