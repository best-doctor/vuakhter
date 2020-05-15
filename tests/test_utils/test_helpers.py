import datetime

import pytest

from vuakhter.utils.helpers import timestamp, is_valid, get_endpoint, deep_get, chunks
from vuakhter.utils.types import RequestEntry


@pytest.mark.parametrize(
    'date, ms, expected_result',
    [
        [datetime.date(2020, 4, 1), False, 1585699200],
        [datetime.date(2020, 4, 1), True, 1585699200000],
        [datetime.datetime(2020, 4, 1, 12, 12, 12), False, 1585743132],
        [datetime.datetime(2020, 4, 1, 12, 12, 12), True, 1585743132000],
    ],
)
def test_timestamp(date, ms, expected_result):
    assert timestamp(date, ms=ms) == expected_result


@pytest.mark.parametrize(
    'entry',
    [
        RequestEntry(ts=0, request_id='', status_code=200, json='{"data": {}}'),
        RequestEntry(ts=0, request_id='', status_code=400, json='{"message": "Validation error"}'),
    ],
)
def test_is_valid_passes(entry):
    assert is_valid(entry) is True


@pytest.mark.parametrize(
    'entry',
    [
        RequestEntry(ts=0, request_id='', status_code=200, json='{"data": {}, "errors": []}'),
        RequestEntry(ts=0, request_id='', status_code=400, json='{"data": {}, "errors": ["Validation error"]}'),
        RequestEntry(ts=0, request_id='', status_code=400, json='{"'),
    ],
)
def test_is_valid_fails(entry):
    assert is_valid(entry) is False


@pytest.mark.parametrize(
    'url, expected_result',
    [
        ['/int/1234/', '/int/_INT_/'],
        ['/int/1234', '/int/_INT_'],
        ['/int/1234/?query', '/int/_INT_/'],
        ['/int/1234?query', '/int/_INT_'],
        ['/float/1234.5?query', '/float/_FLOAT_'],
        ['/uuid/8a44c1ff-0cfa-401e-b2b3-4821a677d103/?query', '/uuid/_UUID_/'],
        ['/1234/54321.0/8a44c1ff-0cfa-401e-b2b3-4821a677d103/?query', '/_INT_/_FLOAT_/_UUID_/'],
    ],
)
def test_get_endpoint(url, expected_result):
    assert get_endpoint(url) == expected_result


@pytest.mark.parametrize(
    'keys, default, expected_result',
    [
        ['level1', None, 1],
        ['level2.level2_1', None, 0],
        ['level1.level1_1', 1, 1],
        ['level2.level2_2', None, 'abcd'],
        ['level3.level3_1', 'abcd', 'abcd'],
    ],
)
def test_deep_get_returns_value(keys, default, expected_result):
    dct = {
        'level1': 1,
        'level2': {
            'level2_1': 0,
            'level2_2': 'abcd',
        },
        'level3': None,
    }

    assert deep_get(dct, keys, default=default) == expected_result


@pytest.mark.parametrize(
    'keys, default',
    [
        ['level1.level1_1', None],
        ['level3', 0],
    ],
)
def test_deep_get_returns_none(keys, default):
    dct = {
        'level1': 1,
        'level2': {
            'level2_1': 0,
            'level2_2': 'abcd',
        },
        'level3': None,
    }

    assert deep_get(dct, keys, default=default) is None


@pytest.mark.parametrize(
    'length, size, chunks_list_size, last_chunk_size',
    [
        [1, 10, 1, 1],
        [11, 10, 2, 1],
        [99, 49, 3, 1],
    ],
)
def test_chunks(length, size, chunks_list_size, last_chunk_size):
    chunk_list = list(chunks(range(1, length + 1), size=size))

    assert len(chunk_list) == chunks_list_size
    assert len(chunk_list[-1]) == last_chunk_size


def test_chunks_zero_length():
    chunk_list = list(chunks(iter([])))

    assert len(chunk_list) == 0
