from __future__ import annotations
from typing import TYPE_CHECKING

from vuakhter.base.requests_log import RequestsLog
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.kibana import gen_request_entries

if TYPE_CHECKING:
    from typing import Any, Iterator, Optional, Sequence
    from vuakhter.utils.types import RequestEntry


class ElasticRequestsLog(ElasticLog, RequestsLog):
    def __init__(self, index_pattern: str = 'django-*', *args: Any, **kwargs: Any):
        super().__init__(index_pattern, *args, **kwargs)

    def gen_entries(self, index: str, request_ids: Optional[Sequence[str]] = None) -> Iterator[RequestEntry]:
        if request_ids:
            yield from gen_request_entries(self.client, index, request_ids)
