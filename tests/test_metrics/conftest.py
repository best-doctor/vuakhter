import pytest

from vuakhter.kibana.requests_log import ElasticRequestsLog
from vuakhter.metrics.counters import (
    MethodCounter, EndpointCounter, ResponseTimeCounter, ComplexCounter,
    StatusCounter, SlowLogCounter, SchemaValidatorCounter,
)
from vuakhter.utils.types import AccessEntry


@pytest.fixture
def access_entries_iterator():
    access_entry_list = [
        AccessEntry(1588975260, '/endpoint/1', 'GET', 200, '1234500', 51.0),
        AccessEntry(1588975261, '/endpoint/1', 'GET', 200, '1234501', 55.0),
        AccessEntry(1588975262, '/endpoint/1/list', 'OPTIONS', 200, '1234502', 5.0),
        AccessEntry(1588975263, '/endpoint/1/list', 'POST', 400, '1234503', 100.0),
        AccessEntry(1588975264, '/endpoint/1/list', 'POST', 200, '1234504', 50.0),
        AccessEntry(1588975265, '/endpoint/1/list', 'GET', 200, '1234505', 45.0),
        AccessEntry(1588975266, '/endpoint/1/list/2', 'PUT', 200, '1234506', 50.0),
        AccessEntry(1588975267, '/endpoint/2', 'GET', 200, '1234507', 45.0),
        AccessEntry(1588975268, '/endpoint/2', 'POST', 403, '1234508', 50.0),
        AccessEntry(1588975269, '/endpoint/2', 'PUT', 200, '1234509', 75.0),
        AccessEntry(1588975270, '/endpoint/2', 'DELETE', 500, '1234510', 150.0),
    ]
    return iter(access_entry_list)


@pytest.fixture()
def counter_instance(access_entries_iterator):
    def get_counter_instance(counter_class, **kwargs):
        counter_instance = counter_class(**kwargs)
        counter_instance.initialize()
        for entry in access_entries_iterator:
            counter_instance.process_entry(entry)
        counter_instance.finalize()
        return counter_instance
    return get_counter_instance


@pytest.fixture()
def method_counter(counter_instance):
    return counter_instance(MethodCounter)


@pytest.fixture()
def endpoint_counter(counter_instance):
    return counter_instance(EndpointCounter)


@pytest.fixture()
def status_counter(counter_instance):
    return counter_instance(StatusCounter)


@pytest.fixture()
def complex_counter(counter_instance):
    return counter_instance(ComplexCounter)


@pytest.fixture()
def response_time_counter(counter_instance, fraction=50.0):
    return counter_instance(ResponseTimeCounter, fraction=fraction)


@pytest.fixture()
def slow_log_counter(counter_instance):
    def get_slow_log_counter(**kwargs):
        return counter_instance(SlowLogCounter, **kwargs)
    return get_slow_log_counter


@pytest.fixture()
def schema_validator_counter(counter_instance, mocked_indices_get):
    mocked_indices_get({})
    requests_log = ElasticRequestsLog()
    return counter_instance(SchemaValidatorCounter, requests_log=requests_log)
