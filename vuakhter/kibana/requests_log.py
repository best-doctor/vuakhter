from __future__ import annotations
import typing

from vuakhter.base.requests_log import RequestsLog
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.kibana import gen_request_entries, filter_by_request_ids

if typing.TYPE_CHECKING:
    from vuakhter.utils.types import RequestEntry, SearchFactory, FilterFunction, GeneratorFunction


class ElasticRequestsLog(ElasticLog, RequestsLog):
    def __init__(
        self, index_pattern: str = 'django-*',
        generator_function: GeneratorFunction = None,
        filter_function: FilterFunction = None,
        *args: typing.Any, **kwargs: typing.Any,
    ):
        generator_function = generator_function or gen_request_entries
        filter_function = filter_function or filter_by_request_ids
        super().__init__(
            index_pattern, generator_function=generator_function, filter_function=filter_function, *args, **kwargs)

    def gen_entries(
        self, index: str, get_search: SearchFactory,
        filter_function: typing.Callable = None,
        **kwargs: typing.Any,
    ) -> typing.Iterator[RequestEntry]:
        request_ids = kwargs.get('request_ids', None)
        if request_ids:
            yield from super().gen_entries(index, get_search, filter_function, **kwargs)
