import datetime
import pytest

from vuakhter.utils.helpers import timestamp
from vuakhter.utils.kibana import (
    get_timestamp, get_indices_for_timeslot, get_access_search,
    get_request_search, get_indicies_aggregation,
)


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
    'min_ts,max_ts,expected_list',
    (
        (
            timestamp(datetime.date(2020, 1, 15)),
            timestamp(datetime.date(2020, 2, 15)),
            ['idx-2020-01', 'idx-2020-02', 'idx-2020-01..02', 'idx-2020-02..03'],
        ),
        (
            timestamp(datetime.date(2020, 3, 1)),
            timestamp(datetime.date(2020, 4, 1)),
            ['idx-2020-03', 'idx-2020-02..03', 'idx-2020-03..04'],
        ),
        (
            timestamp(datetime.date(2019, 3, 1)),
            timestamp(datetime.date(2019, 4, 1)),
            [],
        ),
    ),
)
def test_get_indices_for_timeslot(indices_boundaries, min_ts, max_ts, expected_list):
    indices = get_indices_for_timeslot(indices_boundaries, min_ts, max_ts)

    assert indices == expected_list


@pytest.mark.parametrize(
    'start_ts,end_ts,prefixes,expected',
    (
        (
            None, None, ['/prefix'],
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
            None, None, ['/prefix1', '/prefix2'],
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
            1585699200, 1585743132, [],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'range': {'@timestamp': {'gte': 1585699200, 'lte': 1585743132}}},
                        ],
                    },
                },
            },
        ),
        (
            None, None, [],
            {},
        ),
    ),
)
def test_get_access_query_without_timerange(start_ts, end_ts, prefixes, expected):
    search = get_access_search(None, 'index', start_ts, end_ts, prefixes)

    assert search.to_dict() == expected


@pytest.mark.parametrize(
    'start_ts,end_ts,request_ids,expected',
    (
        (
            None, None, ['requestid'],
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
            None, None, ['requestid1', 'requestid2'],
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
            1585699200, 1585743132, [],
            {
                'query': {
                    'bool': {
                        'filter': [
                            {'range': {'@timestamp': {'gte': 1585699200, 'lte': 1585743132}}},
                        ],
                    },
                },
            },
        ),
        (
            None, None, [],
            {},
        ),
    ),
)
def test_get_request_search(start_ts, end_ts, request_ids, expected):
    search = get_request_search(None, 'index', start_ts, end_ts, request_ids)

    assert search.to_dict() == expected


@pytest.mark.parametrize(
    'expected',
    (
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
)
def test_get_indicies_aggregation(expected):
    search = get_indicies_aggregation(None, [])

    assert search.to_dict() == expected
