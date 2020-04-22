from __future__ import annotations
from typing import TYPE_CHECKING

import collections

if TYPE_CHECKING:
    from typing import Any
    from vuakhter.utils.types import AccessEntry


class StatisticsMetrics:
    description = 'Some metrics'

    def __init__(self) -> None:
        self.initialize()

    @property
    def statistics(self) -> Any:
        return self._statistics

    def initialize(self) -> None:
        self._statistics = collections.defaultdict(int)

    def finalize(self) -> None:
        pass

    def process_entry(self, entry: AccessEntry) -> None:
        raise NotImplementedError()

    def report(self) -> str:
        report = list(
            self.description,
            '-' * len(self.description),
        )
        report.append(f'{self._statistics}')
        for key, value in self._statistics.items():
            report.append(f'{key} {value}')
        return '\n'.join(report)
