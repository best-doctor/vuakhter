import pytest

from tests.responses.indices import indices_get_response, indices_aggregation_response
from vuakhter.kibana.elastic_log import ElasticLog
from vuakhter.utils.types import Boundaries


@pytest.mark.parametrize(
    'expected',
    (
        {
            'index-000005': Boundaries(min_ts=1575376335698.0, max_ts=1575463337966.0),
            'index-000004': Boundaries(min_ts=1575289333416.0, max_ts=1575376342679.0),
            'index-000003': Boundaries(min_ts=1575028332982.0, max_ts=1575115339253.0),
            'index-000002': Boundaries(min_ts=1575202335222.0, max_ts=1575289336569.0),
            'index-000001': Boundaries(min_ts=1575115342163.0, max_ts=1575202338431.0),
        },
    ),
)
def test_elastic_log(mocked_indices_get, mocked_search, expected):
    mocked_indices_get(indices_get_response)
    mocked_search(indices_aggregation_response)
    elastic_log = ElasticLog('index-*')

    assert elastic_log.indices == expected
