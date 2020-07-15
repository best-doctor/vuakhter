from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AnyIterator, TimestampRange


class BaseLog:
    def get_records(self, ts_range: TimestampRange = None, **kwargs: typing.Any) -> AnyIterator:
        raise NotImplementedError()
