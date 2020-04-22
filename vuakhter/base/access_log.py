from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator, Optional, Sequence
    from vuakhter.utils.types import AccessEntry


class AccessLog:
    def get_records(
        self, start_ts: int, end_ts: int, prefixes: Optional[Sequence[str]] = None,
    ) -> Iterator[AccessEntry]:
        raise NotImplementedError()
