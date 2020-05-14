from tests.test_kibana.responses.scan import scan_access_response
from vuakhter.kibana.access_log import ElasticAccessLog


def test_access_log(mocked_scan, mocked_indices_get, mocked_count):
    mocked_scan(scan_access_response)
    mocked_indices_get()
    mocked_count(1)
    access_log = ElasticAccessLog()

    entries = list(access_log.gen_entries('index', prefixes=['/prefix']))

    assert len(entries) == 1
