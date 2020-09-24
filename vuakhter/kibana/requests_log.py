from __future__ import annotations
import typing

from vuakhter.base.requests_log import RequestsLog
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.kibana import gen_request_entries, filter_by_request_ids

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import RequestEntry, TimestampRange, SearchFactory


class ElasticRequestsLog(ElasticLog, RequestsLog):
    def __init__(self, index_pattern: str = 'django-*', *args: typing.Any, **kwargs: typing.Any):
        super().__init__(index_pattern, *args, **kwargs)

    def gen_entries(
        self, index: str, get_search: SearchFactory,
        ts_range: TimestampRange = None,
        filter_function: typing.Callable = None,
        **kwargs: typing.Any,
    ) -> typing.Iterator[RequestEntry]:
        filter_function = filter_function or filter_by_request_ids
        request_ids = kwargs.get('request_ids', None)
        if request_ids:
            yield from gen_request_entries(
                super().gen_entries(index, get_search, ts_range, filter_function, **kwargs),
            )
