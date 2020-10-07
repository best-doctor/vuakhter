from __future__ import annotations
import typing

from vuakhter.base.access_log import AccessLog
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.kibana import gen_access_entries, filter_url_by_prefixes

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import AccessEntry, SearchFactory, FilterFunction, GeneratorFunction


class ElasticAccessLog(ElasticLog, AccessLog):
    def __init__(
        self, index_pattern: str = 'filebeat-*',
        generator_function: GeneratorFunction = None,
        filter_function: FilterFunction = None,
        *args: typing.Any, **kwargs: typing.Any,
    ) -> None:
        generator_function = generator_function or gen_access_entries
        filter_function = filter_function or filter_url_by_prefixes
        super().__init__(
            index_pattern, generator_function=generator_function, filter_function=filter_function, *args, **kwargs)

    def gen_entries(
        self, index: str, get_search: SearchFactory,
        filter_function: typing.Callable = None,
        **kwargs: typing.Any,
    ) -> typing.Iterator[AccessEntry]:
        prefixes = kwargs.get('prefixes', None)
        if prefixes:
            yield from super().gen_entries(index, get_search, filter_function, **kwargs)
