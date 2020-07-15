from __future__ import annotations
import typing

from elasticsearch import Elasticsearch

from vuakhter.base.base_log import BaseLog
from vuakhter.utils.helpers import chunks
from vuakhter.utils.kibana import get_indices_for_timeslot, scan_indices

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import TimestampRange, AnyIterator


class ElasticLog(BaseLog):
    def __init__(
        self, index_pattern: str, client: Elasticsearch = None,
        *args: typing.Any, **kwargs: typing.Any,
    ):
        self.client = client or Elasticsearch(*args, **kwargs)
        self.indices = scan_indices(self.client, index_pattern)

    def gen_entries(self, index: str, ts_range: TimestampRange = None, **kwargs: typing.Any) -> AnyIterator:
        raise NotImplementedError()

    def get_records(self, ts_range: TimestampRange = None, **kwargs: typing.Any) -> AnyIterator:
        indices = get_indices_for_timeslot(self.indices, ts_range)

        for chunk in chunks(indices):
            yield from self.gen_entries(','.join(chunk), ts_range, **kwargs)
