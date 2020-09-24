from __future__ import annotations
import typing

from vuakhter.base.access_log import AccessLog
from vuakhter.kibana.elastic_log import ElasticLog

from vuakhter.utils.kibana import gen_access_entries, filter_url_by_prefixes

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AccessEntry, TimestampRange, SearchFactory


class ElasticAccessLog(ElasticLog, AccessLog):
    def __init__(self, index_pattern: str = 'filebeat-*', *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(index_pattern, *args, **kwargs)

    def gen_entries(
        self, index: str, get_search: SearchFactory,
        ts_range: TimestampRange = None,
        filter_function: typing.Callable = None,
        **kwargs: typing.Any,
    ) -> typing.Iterator[AccessEntry]:
        filter_function = filter_function or filter_url_by_prefixes
        prefixes = kwargs.get('prefixes', None)
        if prefixes:
            yield from gen_access_entries(
                super().gen_entries(index, get_search, ts_range, filter_function, **kwargs),
            )
