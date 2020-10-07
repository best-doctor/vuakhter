from tests.responses.scan import scan_requests_response
from vuakhter.kibana.requests_log import ElasticRequestsLog


def test_requests_log(mocked_scan, mocked_indices_get, mocked_count):
    mocked_scan(scan_requests_response)
    mocked_indices_get()
    mocked_count(1)
    requests_log = ElasticRequestsLog(timestamp_field='@timestamp')

    get_search = requests_log.get_search_factory()
    entries = list(requests_log.gen_entries('index-requests', get_search, request_ids=['request_id_1', 'request_id_2']))

    assert len(entries) == 2
