from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator, Optional, Sequence
    from vuakhter.utils.types import RequestEntry


class RequestsLog:
    def get_records(
        self, start_ts: int, end_ts: int, request_ids: Optional[Sequence[str]] = None,
    ) -> Iterator[RequestEntry]:
        raise NotImplementedError()
