import pytest

from tests.responses.indices import indices_get_response, indices_aggregation_response
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.types import TimestampRange


@pytest.mark.parametrize(
    'expected',
    (
        {
            'index-000005': TimestampRange(1575376335698, 1575463337966),
            'index-000004': TimestampRange(1575289333416, 1575376342679),
            'index-000003': TimestampRange(1575028332982, 1575115339253),
            'index-000002': TimestampRange(1575202335222, 1575289336569),
            'index-000001': TimestampRange(1575115342163, 1575202338431),
        },
    ),
)
def test_elastic_log(mocked_indices_get, mocked_search, expected):
    mocked_indices_get(indices_get_response)
    mocked_search(indices_aggregation_response)
    elastic_log = ElasticLog('index-*')

    assert elastic_log.indices == expected
