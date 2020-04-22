from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
import operator
import logging

from elasticsearch import NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Query, Q

from vuakhter.utils.helpers import chunks, deep_get, timestamp
from vuakhter.utils.types import Boundaries, AccessEntry, RequestEntry

if TYPE_CHECKING:
    from typing import Iterator, List, Sequence
    from elasticsearch import Elasticsearch
    from vuakhter.utils.types import IndicesBoundaries


logger = logging.getLogger(__name__)


class MatchBoolPrefix(Query):
    name = 'match_bool_prefix'


def get_timestamp(ts_str: str) -> int:
    return timestamp(
        datetime.datetime.fromisoformat(ts_str.rstrip('Z')),
        ms=True,
    )


def gen_access_entries(
        client: Elasticsearch, index: str, prefixes: Sequence[str],
) -> Iterator[AccessEntry]:
    prefix, *tail = prefixes
    query = Q('match_bool_prefix', url__original=prefix)
    for prefix in tail:
        query = query | Q('match_bool_prefix', url__original=prefix)
    search = Search(using=client, index=index).filter(query)

    logger.info('Scan %s with query %s, expect %d results', index, search.to_dict(), search.count())
    for hit in search.scan():
        hit_dict = hit.to_dict()
        try:
            yield AccessEntry(
                ts=get_timestamp(deep_get(hit_dict, '@timestamp')),
                url=deep_get(hit_dict, 'url.original'),
                method=deep_get(hit_dict, 'http.request.method'),
                status_code=int(deep_get(hit_dict, 'http.response.status_code')),
                response_time=float(deep_get(hit_dict, 'http.response.duration')),
                request_id=deep_get(hit_dict, 'nginx.access.request_id'),
            )
        except (KeyError, ValueError, TypeError):
            fail_dict = {
                'ts': deep_get(hit_dict, '@timestamp'),
                'url': deep_get(hit_dict, 'url.original'),
                'method': deep_get(hit_dict, 'http.request.method'),
                'status_code': deep_get(hit_dict, 'http.response.status_code'),
                'response_time': deep_get(hit_dict, 'http.response.duration'),
                'request_id': deep_get(hit_dict, 'nginx.access.request_id'),
            }
            logger.debug('Failed with %s', fail_dict)
            pass


def gen_request_entries(
        client: Elasticsearch, index: str, request_ids: Sequence[str],
) -> Iterator[RequestEntry]:
    search = Search(using=client, index=index)
    search = (
        search.filter('term', response__type='json_response_log')
              .filter('terms', response__request_id=request_ids)
    )

    logger.info('Scan %s with query %s, expect %d results', index, search.to_dict(), search.count())
    for hit in search.scan():
        hit_dict = hit.to_dict()
        try:
            yield RequestEntry(
                ts=get_timestamp(deep_get(hit_dict, '@timestamp')),
                json=deep_get(hit_dict, 'response.json'),
                request_id=deep_get(hit_dict, 'response.request_id'),
                status_code=int(deep_get(hit_dict, 'response.status')),
            )
        except (KeyError, ValueError, TypeError):
            fail_dict = {
                'ts': deep_get(hit_dict, '@timestamp'),
                'json': deep_get(hit_dict, 'response.json'),
                'request_id': deep_get(hit_dict, 'response.request_id'),
                'status_code': deep_get(hit_dict, 'response.status'),
            }
            logger.debug('Failed with %s', fail_dict)
            pass


def get_indices_for_timeslot(indices: IndicesBoundaries, start_ts: int, end_ts: int) -> List[str]:
    indices_names = []
    for name, boundaries in indices.items():
        if boundaries.max_ts <= start_ts or boundaries.min_ts >= end_ts:
            continue
        indices_names.append(name)
    return indices_names


def scan_indices(client: Elasticsearch, index_pattern: str) -> IndicesBoundaries:
    try:
        indices_dict = client.indices.get(index_pattern)
    except NotFoundError:
        indices_dict = {}

    indices_list = []

    for chunk in chunks(indices_dict.keys()):
        search = Search(using=client, index=','.join(chunk))[0:0]
        (
            search.aggs
                  .bucket('index', 'terms', field='_index')
                  .metric('min_ts', 'min', field='@timestamp')
                  .metric('max_ts', 'max', field='@timestamp')
        )
        result = search.execute()
        buckets = result.aggregations.index.buckets
        for bucket in buckets:
            indices_list.append(
                (bucket.key, bucket.min_ts.value, bucket.max_ts.value),
            )
    return {
        index: Boundaries(min_ts=min_ts, max_ts=max_ts)
        for index, min_ts, max_ts
        in sorted(indices_list, key=operator.itemgetter(1), reverse=True)
    }
