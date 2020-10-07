from __future__ import annotations
import logging
import typing

from elasticsearch import Elasticsearch

from vuakhter.base.base_log import BaseLog
from vuakhter.utils.helpers import chunks
from vuakhter.utils.kibana import get_indices_for_timeslot, scan_indices, search_factory

if typing.TYPE_CHECKING:
    from elasticsearch_dsl import Search
    from vuakhter.utils.types import (
        TimestampRange, AnyIterator, SearchFactory, AnyIterable,
        EntriesGeneratorFunctions, GeneratorFunction, FilterFunction,
    )

logger = logging.getLogger(__name__)


def passthrough_generator(hits: AnyIterable, timestamp_field: str = None) -> AnyIterator:
    yield from hits


def passthrough_filter(search: Search, **kwargs: typing.Any) -> Search:
    return search


class EntriesGenerator:
    def __init__(self, generator_function: GeneratorFunction = None, filter_function: FilterFunction = None) -> None:
        self.functions: EntriesGeneratorFunctions = {
            'generator_function': generator_function or passthrough_generator,
            'filter_function': filter_function or passthrough_filter,
        }

    @property
    def generator_function(self) -> GeneratorFunction:
        return self.functions['generator_function']

    @property
    def filter_function(self) -> FilterFunction:
        return self.functions['filter_function']


class ElasticLog(EntriesGenerator, BaseLog):
    def __init__(
        self, index_pattern: str, client: Elasticsearch = None,
        timestamp_field: str = None,
        *args: typing.Any, **kwargs: typing.Any,
    ):
        timestamp_field = timestamp_field or 'timestamp'
        self.client = client or Elasticsearch(*args, **kwargs)
        self.indices = scan_indices(self.client, index_pattern, timestamp_field)
        self.timestamp_field = timestamp_field

        super().__init__(*args, **kwargs)

    def get_search_factory(self, ts_range: TimestampRange = None) -> SearchFactory:
        return search_factory(self.client, ts_range)

    def gen_entries(
        self, index: str, get_search: SearchFactory,
        filter_function: typing.Callable = None,
        **kwargs: typing.Any,
    ) -> AnyIterator:
        search = get_search(index)
        filter_function = filter_function or self.filter_function
        if filter_function:
            search = filter_function(search, **kwargs)
        logger.info('Scan %s with query %s, expect %d results', index, search.to_dict(), search.count())
        yield from self.generator_function(search.scan(), self.timestamp_field)

    def get_records(
        self, ts_range: TimestampRange = None, **kwargs: typing.Any,
    ) -> AnyIterator:
        indices = get_indices_for_timeslot(self.indices, ts_range)

        for chunk in chunks(indices):
            yield from self.gen_entries(
                ','.join(chunk), self.get_search_factory(ts_range), **kwargs)
