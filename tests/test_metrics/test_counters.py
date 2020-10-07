import pytest


def test_method_counter(method_counter):
    assert method_counter.statistics == {
        'GET': 4,
        'POST': 3,
        'PUT': 2,
        'DELETE': 1,
        'OPTIONS': 1,
    }


def test_endpoint_counter(endpoint_counter):
    assert endpoint_counter.statistics == {
        '/endpoint/_INT_': 6,
        '/endpoint/_INT_/list': 4,
        '/endpoint/_INT_/list/_INT_': 1,
    }


def test_status_counter(status_counter):
    assert status_counter.statistics == {
        200: 8,
        400: 1,
        403: 1,
        500: 1,
    }


def test_response_time_counter(response_time_counter):
    assert response_time_counter.statistics == {
        50.0: 6,
        100.0: 4,
        150.0: 1,
    }


def test_complex_counter(complex_counter):
    assert complex_counter.statistics == {
        ('/endpoint/_INT_', 'GET', 200): 3,
        ('/endpoint/_INT_', 'DELETE', 500): 1,
        ('/endpoint/_INT_', 'POST', 403): 1,
        ('/endpoint/_INT_', 'PUT', 200): 1,
        ('/endpoint/_INT_/list', 'GET', 200): 1,
        ('/endpoint/_INT_/list', 'OPTIONS', 200): 1,
        ('/endpoint/_INT_/list', 'POST', 200): 1,
        ('/endpoint/_INT_/list', 'POST', 400): 1,
        ('/endpoint/_INT_/list/_INT_', 'PUT', 200): 1,
    }


@pytest.mark.parametrize(
    'top,mangle,expected_top,expected_report',
    (
        (
            2, False, [('/endpoint/2', 150.0), ('/endpoint/1/list', 100.0)],
            '/endpoint/2 150.0\n/endpoint/1/list 100.0',
        ),
        (
            2, True, [('/endpoint/_INT_', 150.0), ('/endpoint/_INT_/list', 100.0)],
            '/endpoint/_INT_ 150.0\n/endpoint/_INT_/list 100.0',
        ),
    ),
)
def test_slow_log_counter_mangle(slow_log_counter, top, mangle, expected_top, expected_report):
    counter = slow_log_counter(top=top, mangle=mangle)

    assert counter.statistics['top'] == expected_top
    assert counter.report() == expected_report


def test_schema_validator_counter(schema_validator_counter):
    assert schema_validator_counter.statistics == {'invalid': 0, 'missed': 10, 'valid': 0}
    assert schema_validator_counter.report() == 'Valid requests 0.00% (0 out of 0, 10 missed)'
