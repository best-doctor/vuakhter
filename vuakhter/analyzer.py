from __future__ import annotations
from typing import TYPE_CHECKING

from vuakhter.utils.helpers import timestamp

if TYPE_CHECKING:
    from typing import Optional, Dict, List, Sequence
    from vuakhter.base.access_log import AccessLog
    from vuakhter.metrics.base import StatisticsMetrics
    from vuakhter.utils.types import DateOrDatetime


class HttpAnalyzer:
    def __init__(
            self, access_log: AccessLog,
            prefixes: Optional[Sequence[str]] = None,
            metrics: Optional[Sequence[StatisticsMetrics]] = None,
    ) -> None:
        self.access_log = access_log
        self.prefixes = prefixes or ['/']
        metrics = metrics or []
        self._metrics: List[StatisticsMetrics] = metrics

    @property
    def metrics(self) -> List[StatisticsMetrics]:
        return self._metrics

    def add_metric(self, metric: StatisticsMetrics):
        self._metrics.append(metric)

    def analyze(self, start_date: DateOrDatetime, end_date: DateOrDatetime) -> Dict:
        if not self._metrics:
            return

        start_ts = timestamp(start_date, ms=True)
        end_ts = timestamp(end_date, ms=True)

        for metric in self._metrics:
            metric.initialize()

        for entry in self.access_log.get_records(start_ts, end_ts, prefixes=self.prefixes):
            for metric in self._metrics:
                metric.process_entry(entry)
