from __future__ import annotations
import logging
import typing

from elasticsearch import Elasticsearch

from vuakhter.base.base_log import BaseLog
from vuakhter.utils.helpers import chunks
from vuakhter.utils.kibana import get_indices_for_timeslot, scan_indices, search_factory

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import TimestampRange, AnyIterator, SearchFactory

logger = logging.getLogger(__name__)


class ElasticLog(BaseLog):
    def __init__(
        self, index_pattern: str, client: Elasticsearch = None,
        timestamp_field: str = 'timestamp', *args: typing.Any, **kwargs: typing.Any,
    ):

        self.client = client or Elasticsearch(*args, **kwargs)
        self.indices = scan_indices(self.client, index_pattern, timestamp_field)

    def get_search_factory(self, ts_range: TimestampRange = None) -> SearchFactory:
        return search_factory(self.client, ts_range)

    def gen_entries(
        self, index: str, get_search: SearchFactory,
        ts_range: TimestampRange = None,
        filter_function: typing.Callable = None,
        **kwargs: typing.Any,
    ) -> AnyIterator:
        search = get_search(index)
        if filter_function:
            search = filter_function(search, **kwargs)
        logger.info('Scan %s with query %s, expect %d results', index, search.to_dict(), search.count())
        yield from search.scan()

    def get_records(
        self, ts_range: TimestampRange = None, **kwargs: typing.Any,
    ) -> AnyIterator:
        indices = get_indices_for_timeslot(self.indices, ts_range)

        for chunk in chunks(indices):
            yield from self.gen_entries(
                ','.join(chunk), self.get_search_factory(ts_range), **kwargs)
