from __future__ import annotations
import typing

from vuakhter.base.access_log import AccessLog
from vuakhter.kibana.elastic_log import ElasticLog

from vuakhter.utils.kibana import gen_access_entries

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AccessEntry


class ElasticAccessLog(ElasticLog, AccessLog):
    def __init__(self, index_pattern: str = 'filebeat-*', *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(index_pattern, *args, **kwargs)

    def gen_entries(self, index: str, **kwargs: typing.Any) -> typing.Iterator[AccessEntry]:
        prefixes = kwargs.pop('prefixes', None)
        if prefixes:
            yield from gen_access_entries(self.client, index, prefixes)
