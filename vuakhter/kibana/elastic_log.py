from __future__ import annotations
import typing

from vuakhter.utils.helpers import chunks
from vuakhter.utils.kibana import get_indices_for_timeslot, scan_indices

if typing.TYPE_CHECKING:
    from elasticsearch import Elasticsearch
    AnyIterator = typing.Iterator[typing.Any]


class ElasticLog:
    def __init__(
            self, index_pattern: str, client: Elasticsearch = None,
            *args: typing.Any, **kwargs: typing.Any,
    ):
        self.client = client or Elasticsearch(*args, **kwargs)
        self.indices = scan_indices(self.client, index_pattern)

    def gen_entries(self, index: str, **kwargs: typing.Any) -> AnyIterator:
        raise NotImplementedError()

    def get_records(self, start_ts: int, end_ts: int, **kwargs: typing.Any) -> AnyIterator:
        indices = get_indices_for_timeslot(self.indices, start_ts, end_ts)

        for chunk in chunks(indices):
            yield from self.gen_entries(','.join(chunk), **kwargs)
