from __future__ import annotations
import datetime
import typing
import sys

from elasticsearch_dsl import Search

from vuakhter.utils.helpers import timestamp

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


DateOrDatetime = typing.Union[datetime.date, datetime.datetime]


class TimestampRange(typing.NamedTuple):
    start_ts: typing.Optional[int] = None
    end_ts: typing.Optional[int] = None

    @classmethod
    def from_datetime(
        cls, start_date: DateOrDatetime = None, end_date: DateOrDatetime = None, ms: bool = False,
    ) -> TimestampRange:
        start_ts = timestamp(start_date, ms=ms) if start_date else None
        end_ts = timestamp(end_date, ms=ms) if end_date else None

        return cls(start_ts, end_ts)

    @classmethod
    def from_datetime_and_timedelta(
        cls, end_date: DateOrDatetime = None, timedelta: datetime.timedelta = None, ms: bool = False,
    ) -> TimestampRange:
        timedelta = timedelta or datetime.timedelta(hours=24)
        end_date = end_date or datetime.datetime.utcnow()
        start_date = end_date - timedelta
        if start_date > end_date:
            return cls.from_datetime(end_date, start_date, ms=ms)
        return cls.from_datetime(start_date, end_date, ms=ms)

    def overlaps(self, other: TimestampRange, strict: bool = False) -> bool:
        if not (self.start_ts and self.end_ts and other.start_ts and other.end_ts):
            return not strict
        if self.end_ts <= other.start_ts or self.start_ts >= other.end_ts:
            return False
        return True


class AccessEntry(typing.NamedTuple):
    ts: int
    url: str
    method: str
    status_code: int
    request_id: str
    response_time: float


class RequestEntry(typing.NamedTuple):
    ts: int
    json: str
    request_id: str
    status_code: int


IndicesBoundaries = typing.Dict[str, TimestampRange]

AccessEntryIterator = typing.Iterator[AccessEntry]

RequestEntryIterator = typing.Iterator[RequestEntry]

AnyIterator = typing.Iterator[typing.Any]
AnyIterable = typing.Iterable[typing.Any]

SearchFactory = typing.Callable[[str], Search]

GeneratorFunction = typing.Callable[[AnyIterable, typing.Optional[str]], AnyIterator]
FilterFunction = typing.Callable


class EntriesGeneratorFunctions(TypedDict):
    generator_function: GeneratorFunction
    filter_function: FilterFunction
