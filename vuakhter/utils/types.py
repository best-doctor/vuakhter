from __future__ import annotations
import datetime
import typing


class Boundaries(typing.NamedTuple):
    min_ts: float
    max_ts: float


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


DateOrDatetime = typing.Union[datetime.date, datetime.datetime]

IndicesBoundaries = typing.Dict[str, Boundaries]


class LoggingConfig(typing.TypedDict, total=False):
    version: int
    disable_existing_loggers: bool
    handlers: typing.Dict[str, typing.Dict]
    formatters: typing.Dict[str, typing.Dict]
    loggers: typing.Dict[str, typing.Dict]
    root: typing.Dict
