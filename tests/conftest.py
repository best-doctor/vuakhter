import pytest
from elasticsearch.client import IndicesClient, Elasticsearch


@pytest.fixture
def mocked_scan(mocker):
    def get_mocked_scan(response=None):
        mocked_scan = mocker.patch('elasticsearch_dsl.search.scan')
        return_value = None
        if response and response['hits'] and response['hits']['hits']:
            return_value = iter(response['hits']['hits'])
        mocked_scan.return_value = return_value
        return mocked_scan
    return get_mocked_scan


@pytest.fixture
def mocked_search(mocker):
    def get_mocked_search(response=None):
        mocked_search = mocker.patch.object(Elasticsearch, 'search')
        mocked_search.return_value = response
        return mocked_search
    return get_mocked_search


@pytest.fixture
def mocked_indices_get(mocker):
    def get_mocked_indices_get(response=None):
        mocked_indices_get = mocker.patch.object(IndicesClient, 'get')
        mocked_indices_get.return_value = response or {}
        return mocked_indices_get
    return get_mocked_indices_get


@pytest.fixture
def mocked_count(mocker):
    def get_mocked_count(count=0):
        mocked_count = mocker.patch.object(Elasticsearch, 'count')
        mocked_count.return_value = {'count': count}
        return mocked_count
    return get_mocked_count
