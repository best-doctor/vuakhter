from __future__ import annotations
import typing

from vuakhter.base.base_log import BaseLog

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AccessEntry, TimestampRange


class AccessLog(BaseLog):
    def get_records(self, ts_range: TimestampRange = None, **kwargs: typing.Any) -> typing.Iterator[AccessEntry]:
        raise NotImplementedError()
