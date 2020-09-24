import datetime
import pytest

from vuakhter.utils.helpers import timestamp
from vuakhter.utils.kibana import (
    get_timestamp, get_indices_for_timeslot, get_access_search,
    get_request_search, get_indices_aggregation,
)
from vuakhter.utils.types import TimestampRange


@pytest.mark.parametrize(
    'ts_str,expected_ts',
    (
        ('2020-04-12T06:07:00', 1586671620000),
        ('2020-05-08T22:01:00.654', 1588975260654),
    ),
)
def test_get_timestamp(ts_str, expected_ts):
    result = get_timestamp(ts_str)

    assert result == expected_ts


@pytest.mark.parametrize(
    'ts_range,expected_list',
    (
        (
            TimestampRange(
                timestamp(datetime.date(2020, 1, 15), ms=True), timestamp(datetime.date(2020, 2, 15), ms=True),
            ),
            ['idx-2020-01', 'idx-2020-02', 'idx-2020-01..02', 'idx-2020-02..03'],
        ),
        (
            TimestampRange(
                timestamp(datetime.date(2020, 3, 1), ms=True),
                timestamp(datetime.date(2020, 4, 1), ms=True),
            ),
            ['idx-2020-03', 'idx-2020-02..03', 'idx-2020-03..04'],
        ),
        (
            TimestampRange(
                timestamp(datetime.date(2019, 3, 1), ms=True),
                timestamp(datetime.date(2019, 4, 1), ms=True),
            ),
            [],
        ),
    ),
)
def test_get_indices_for_timeslot(indices_boundaries, ts_range, expected_list):
    indices = get_indices_for_timeslot(indices_boundaries, ts_range)

    assert indices == expected_list


@pytest.mark.parametrize(
    'ts_range,prefixes,expected',
    (
        (
            TimestampRange(None, None), ['/prefix'],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'match_bool_prefix': {'url.original': '/prefix'}},
                        ],
                    },
                },
            },
        ),
        (
            None, ['/prefix1', '/prefix2'],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {
                                'bool': {
                                    'should': [
                                        {'match_bool_prefix': {'url.original': '/prefix1'}},
                                        {'match_bool_prefix': {'url.original': '/prefix2'}},
                                    ],
                                },
                            },
                        ],
                    },
                },
            },
        ),
        (
            TimestampRange(1585699200000, 1585743132000), [],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'range': {'@timestamp': {'gte': 1585699200000, 'lte': 1585743132000}}},
                        ],
                    },
                },
            },
        ),
        (
            TimestampRange(None, None), [],
            {},
        ),
    ),
)
def test_get_access_query_without_timerange(ts_range, prefixes, expected):
    search = get_access_search(None, 'index', ts_range, prefixes, timestamp_field='@timestamp')

    assert search.to_dict() == expected


@pytest.mark.parametrize(
    'ts_range,request_ids,expected',
    (
        (
            None, ['requestid'],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'term': {'response.type': 'json_response_log'}},
                            {
                                'terms': {
                                    'response.request_id': ['requestid'],
                                },
                            },
                        ],
                    },
                },
            },
        ),
        (
            None, ['requestid1', 'requestid2'],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'term': {'response.type': 'json_response_log'}},
                            {
                                'terms': {
                                    'response.request_id': ['requestid1', 'requestid2'],
                                },
                            },
                        ],
                    },
                },
            },
        ),
        (
            TimestampRange(1585699200000, 1585743132000), [],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'range': {'@timestamp': {'gte': 1585699200000, 'lte': 1585743132000}}},
                        ],
                    },
                },
            },
        ),
        (
            TimestampRange(None, None), [],
            {},
        ),
    ),
)
def test_get_request_search(ts_range, request_ids, expected):
    search = get_request_search(None, 'index', ts_range, request_ids, timestamp_field='@timestamp')

    assert search.to_dict() == expected


@pytest.mark.parametrize(
    'timestamp_field,expected',
    (
        (
            '@timestamp',
            {
                'aggs': {
                    'index': {
                        'terms': {'field': '_index'},
                        'aggs': {
                            'min_ts': {'min': {'field': '@timestamp'}},
                            'max_ts': {'max': {'field': '@timestamp'}},
                        },
                    },
                },
                'from': 0,
                'size': 0,
            },
        ),
        (
            'timestamp',
            {
                'aggs': {
                    'index': {
                        'terms': {'field': '_index'},
                        'aggs': {
                            'min_ts': {'min': {'field': 'timestamp'}},
                            'max_ts': {'max': {'field': 'timestamp'}},
                        },
                    },
                },
                'from': 0,
                'size': 0,
            },
        ),
    ),
)
def test_get_indices_aggregation(timestamp_field, expected):
    search = get_indices_aggregation(None, [], timestamp_field=timestamp_field)

    assert search.to_dict() == expected
