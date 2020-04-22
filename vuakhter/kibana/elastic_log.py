from __future__ import annotations
from typing import TYPE_CHECKING

from vuakhter.utils.helpers import chunks
from vuakhter.utils.kibana import get_indices_for_timeslot, scan_indices

if TYPE_CHECKING:
    from typing import Any, Optional, Iterator
    from elasticsearch import Elasticsearch


class ElasticLog:
    def __init__(
            self, index_pattern: str, client: Optional[Elasticsearch] = None,
            *args: Any, **kwargs: Any,
    ):
        self.client = client or Elasticsearch(*args, **kwargs)
        self.indices = scan_indices(self.client, index_pattern)

    def gen_entries(self, index: str, **kwargs: Any) -> Iterator[Any]:
        raise NotImplementedError()

    def get_records(self, start_ts: int, end_ts: int, **kwargs: Any) -> Iterator[Any]:
        indices = get_indices_for_timeslot(self.indices, start_ts, end_ts)

        for chunk in chunks(indices):
            yield from self.gen_entries(','.join(chunk), **kwargs)
