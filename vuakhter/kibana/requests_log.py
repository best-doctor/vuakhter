from __future__ import annotations
import typing

from vuakhter.base.requests_log import RequestsLog
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.kibana import gen_request_entries

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import RequestEntry


class ElasticRequestsLog(ElasticLog, RequestsLog):
    def __init__(self, index_pattern: str = 'django-*', *args: typing.Any, **kwargs: typing.Any):
        super().__init__(index_pattern, *args, **kwargs)

    def gen_entries(self, index: str, **kwargs: typing.Any) -> typing.Iterator[RequestEntry]:
        request_ids = kwargs.pop('request_ids', None)
        if request_ids:
            yield from gen_request_entries(self.client, index, request_ids)
