import datetime
import pytest

from vuakhter.utils.helpers import timestamp
from vuakhter.utils.kibana import get_timestamp, get_indices_for_timeslot


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
    )
)
def test_get_indices_for_timeslot(indices_boundaries, min_ts, max_ts, expected_list):
    indices = get_indices_for_timeslot(indices_boundaries, min_ts, max_ts)

    assert indices == expected_list

