from __future__ import annotations
from typing import TYPE_CHECKING

from vuakhter.base.access_log import AccessLog
from vuakhter.kibana.elastic_log import ElasticLog

from vuakhter.utils.kibana import gen_access_entries

if TYPE_CHECKING:
    from typing import Any, Iterator, Optional, Sequence
    from vuakhter.utils.types import AccessEntry


class ElasticAccessLog(ElasticLog, AccessLog):
    def __init__(self, index_pattern: str = 'filebeat-*', *args: Any, **kwargs: Any):
        super().__init__(index_pattern=index_pattern, *args, **kwargs)

    def gen_entries(self, index: str, prefixes: Optional[Sequence[str]] = None) -> Iterator[AccessEntry]:
        if prefixes:
            yield from gen_access_entries(self.client, index, prefixes)
