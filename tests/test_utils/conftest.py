import datetime

import pytest

from vuakhter.utils.helpers import timestamp
from vuakhter.utils.types import TimestampRange


@pytest.fixture
def indices_boundaries():
    indices_list = [
        (
            'idx-2020-01',
            timestamp(datetime.date(2020, 1, 1), ms=True), timestamp(datetime.date(2020, 2, 1), ms=True),
        ),
        (
            'idx-2020-02',
            timestamp(datetime.date(2020, 2, 1), ms=True), timestamp(datetime.date(2020, 3, 1), ms=True)
        ),
        (
            'idx-2020-03',
            timestamp(datetime.date(2020, 3, 1), ms=True), timestamp(datetime.date(2020, 4, 1), ms=True),
        ),
        (
            'idx-2020-04',
            timestamp(datetime.date(2020, 4, 1), ms=True), timestamp(datetime.date(2020, 5, 1), ms=True),
        ),
        (
            'idx-2020-05',
            timestamp(datetime.date(2020, 5, 1), ms=True), timestamp(datetime.date(2020, 6, 1), ms=True),
        ),
        (
            'idx-2020-01..02',
            timestamp(datetime.date(2020, 1, 1), ms=True), timestamp(datetime.date(2020, 3, 1), ms=True),
        ),
        (
            'idx-2020-02..03',
            timestamp(datetime.date(2020, 2, 1), ms=True), timestamp(datetime.date(2020, 4, 1), ms=True),
        ),
        (
            'idx-2020-03..04',
            timestamp(datetime.date(2020, 3, 1), ms=True), timestamp(datetime.date(2020, 5, 1), ms=True),
        ),
        (
            'idx-2020-04..05',
            timestamp(datetime.date(2020, 4, 1), ms=True), timestamp(datetime.date(2020, 6, 1), ms=True),
        ),
    ]
    return {
        index: TimestampRange(min_ts, max_ts)
        for index, min_ts, max_ts
        in indices_list
    }
