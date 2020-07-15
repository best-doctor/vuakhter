from __future__ import annotations
import typing

from vuakhter.base.base_log import BaseLog

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import RequestEntry, TimestampRange


class RequestsLog(BaseLog):
    def get_records(self, ts_range: TimestampRange = None, **kwargs: typing.Any) -> typing.Iterator[RequestEntry]:
        raise NotImplementedError()
