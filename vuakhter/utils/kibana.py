from __future__ import annotations

import datetime
import typing
import operator
import logging

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Query, Q

from vuakhter.utils.helpers import chunks, deep_get, timestamp
from vuakhter.utils.types import AccessEntry, RequestEntry, TimestampRange

if typing.TYPE_CHECKING:
    from elasticsearch import Elasticsearch
    from vuakhter.utils.types import (
        IndicesBoundaries, AccessEntryIterator, RequestEntryIterator, SearchFactory, AnyIterable,
    )


logger = logging.getLogger(__name__)


class MatchBoolPrefix(Query):
    name = 'match_bool_prefix'


def get_timestamp(ts_str: str) -> int:
    return timestamp(
        datetime.datetime.fromisoformat(ts_str.rstrip('Z')),
        ms=True,
    )


def get_range_filter(ts_range: TimestampRange = None, timestamp_field: str = 'timestamp') -> typing.Optional[Q]:
    if ts_range:
        lookup = {}
        if ts_range.start_ts:
            lookup['gte'] = ts_range.start_ts
        if ts_range.end_ts:
            lookup['lte'] = ts_range.end_ts
        if len(lookup):
            return Q('range', **{timestamp_field: lookup})


def search_factory(
    client: Elasticsearch, ts_range: TimestampRange = None, timestamp_field: str = 'timestamp',
) -> SearchFactory:
    range_filter = get_range_filter(ts_range, timestamp_field)

    def get_search(index: str) -> Search:
        search = Search(using=client, index=index)
        if range_filter:
            search = search.filter(range_filter)
        return search

    return get_search


def filter_url_by_prefixes(
    search: Search, prefixes: typing.Sequence[str] = None, url_field: str = 'url__original',
) -> Search:
    if prefixes:
        prefix, *tail = prefixes
        lookup = {url_field: prefix}
        query = Q('match_bool_prefix', **lookup)
        for prefix in tail:
            lookup[url_field] = prefix
            query = query | Q('match_bool_prefix', **lookup)
        search = search.filter(query)
    return search


def get_access_search(
    client: Elasticsearch, index: str, ts_range: TimestampRange = None,
    prefixes: typing.Sequence[str] = None,
    timestamp_field: str = 'timestamp',
) -> Search:
    search = Search(using=client, index=index)
    search = filter_url_by_prefixes(search, prefixes)
    range_filter = get_range_filter(ts_range, timestamp_field)
    if range_filter:
        search = search.filter(range_filter)
    return search


def gen_access_entries(hits: AnyIterable, timestamp_field: str = None) -> AccessEntryIterator:
    timestamp_field = timestamp_field or 'timestamp'
    for hit in hits:
        hit_dict = hit.to_dict()
        try:
            yield AccessEntry(
                ts=get_timestamp(deep_get(hit_dict, timestamp_field)),
                url=deep_get(hit_dict, 'url.original'),
                method=deep_get(hit_dict, 'http.request.method'),
                status_code=int(deep_get(hit_dict, 'http.response.status_code')),
                response_time=float(deep_get(hit_dict, 'http.response.duration', 0)),
                request_id=deep_get(hit_dict, 'nginx.access.request_id'),
            )
        except (KeyError, ValueError, TypeError):
            fail_dict = {
                'ts': deep_get(hit_dict, timestamp_field),
                'url': deep_get(hit_dict, 'url.original'),
                'method': deep_get(hit_dict, 'http.request.method'),
                'status_code': deep_get(hit_dict, 'http.response.status_code'),
                'response_time': deep_get(hit_dict, 'http.response.duration'),
                'request_id': deep_get(hit_dict, 'nginx.access.request_id'),
            }
            logger.debug('Failed with %s', fail_dict)
            pass


def filter_by_request_ids(
    search: Search, request_ids: typing.Sequence[str] = None,
) -> Search:
    if request_ids:
        search = (
            search.filter('term', response__type='json_response_log')
                  .filter('terms', response__request_id=request_ids)
        )
    return search


def get_request_search(
    client: Elasticsearch, index: str, ts_range: TimestampRange = None,
    request_ids: typing.Sequence[str] = None,
    timestamp_field: str = 'timestamp',
) -> Search:
    search = Search(using=client, index=index)
    search = filter_by_request_ids(search, request_ids)
    range_filter = get_range_filter(ts_range, timestamp_field)
    if range_filter:
        search = search.filter(range_filter)
    return search


def gen_request_entries(hits: AnyIterable, timestamp_field: str = None) -> RequestEntryIterator:
    timestamp_field = timestamp_field or 'timestamp'
    for hit in hits:
        hit_dict = hit.to_dict()
        try:
            yield RequestEntry(
                ts=get_timestamp(deep_get(hit_dict, timestamp_field)),
                json=deep_get(hit_dict, 'response.json'),
                request_id=deep_get(hit_dict, 'response.request_id'),
                status_code=int(deep_get(hit_dict, 'response.status')),
            )
        except (KeyError, ValueError, TypeError):
            fail_dict = {
                'ts': deep_get(hit_dict, timestamp_field),
                'json': deep_get(hit_dict, 'response.json'),
                'request_id': deep_get(hit_dict, 'response.request_id'),
                'status_code': deep_get(hit_dict, 'response.status'),
            }
            logger.debug('Failed with %s', fail_dict)
            pass


def get_indices_for_timeslot(indices: IndicesBoundaries, ts_range: TimestampRange = None) -> typing.List[str]:
    indices_names = []
    if ts_range:
        for name, boundaries in indices.items():
            if not ts_range.overlaps(boundaries):
                continue
            indices_names.append(name)
    return indices_names


def get_indices_aggregation(
    client: Elasticsearch, indices: typing.List[str], timestamp_field: str = 'timestamp',
) -> Search:
    search = Search(using=client, index=','.join(indices))[0:0]
    (
        search.aggs
              .bucket('index', 'terms', field='_index')
              .metric('min_ts', 'min', field=timestamp_field)
              .metric('max_ts', 'max', field=timestamp_field)
    )
    return search


def scan_indices(client: Elasticsearch, index_pattern: str, timestamp_field: str = 'timestamp') -> IndicesBoundaries:
    try:
        indices_dict = client.indices.get(index_pattern)
    except NotFoundError:
        indices_dict = {}
    indices_list = []

    for chunk in chunks(indices_dict.keys()):
        search = get_indices_aggregation(client, chunk, timestamp_field)
        result = search.execute()
        buckets = result.aggregations.index.buckets
        for bucket in buckets:
            try:
                indices_list.append(
                    (bucket.key, int(bucket.min_ts.value), round(bucket.max_ts.value)),
                )
            except TypeError:
                logger.debug(
                    'Wrong aggregation results for index %s, min_ts %s, max_ts %s',
                    bucket.key, bucket.min_ts.value, bucket.max_ts.value,
                )
    return {
        index: TimestampRange(start_ts=min_ts, end_ts=max_ts)
        for index, min_ts, max_ts
        in sorted(indices_list, key=operator.itemgetter(1), reverse=True)
    }
