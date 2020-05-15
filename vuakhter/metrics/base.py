from __future__ import annotations
import typing
import collections

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AccessEntry
    StatisticsMapping = typing.Dict[typing.Any, typing.Any]


class StatisticsMetrics:
    _description = 'Some metrics'

    def __init__(self) -> None:
        self.initialize()

    @property
    def description(self) -> str:
        return self._description

    @property
    def statistics(self) -> StatisticsMapping:
        return self._statistics

    def initialize(self) -> None:
        self._statistics: StatisticsMapping = collections.defaultdict(int)

    def finalize(self) -> None:
        pass

    def process_entry(self, entry: AccessEntry) -> None:
        raise NotImplementedError()

    def report(self) -> str:
        report = [self.description, '-' * len(self.description)]
        for key, value in self._statistics.items():
            report.append(f'{key} {value}')
        return '\n'.join(report)
