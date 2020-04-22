from __future__ import annotations
import datetime
from typing import Dict, Union, NamedTuple


class Boundaries(NamedTuple):
    min_ts: float
    max_ts: float


class AccessEntry(NamedTuple):
    ts: int
    url: str
    method: str
    status_code: int
    request_id: str
    response_time: float


class RequestEntry(NamedTuple):
    ts: int
    json: str
    request_id: str
    status_code: int


DateOrDatetime = Union[datetime.date, datetime.datetime]

IndicesBoundaries = Dict[str, Boundaries]
