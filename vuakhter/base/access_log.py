from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AccessEntry


class AccessLog:
    def get_records(self, start_ts: int, end_ts: int, **kwargs: typing.Any) -> typing.Iterator[AccessEntry]:
        raise NotImplementedError()
