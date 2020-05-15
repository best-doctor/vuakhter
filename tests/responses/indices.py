indices_get_response = {
    'index-000005': {},
    'index-000004': {},
    'index-000003': {},
    'index-000002': {},
    'index-000001': {},
}

indices_aggregation_response = {
    'took': 6,
    'timed_out': False,
    '_shards': {'total': 5, 'successful': 5, 'skipped': 0, 'failed': 0},
    'hits': {
        'total': {'value': 10000, 'relation': 'gte'},
        'max_score': None,
        'hits': [],
    },
    'aggregations': {
        'index': {
            'doc_count_error_upper_bound': 0,
            'sum_other_doc_count': 0,
            'buckets': [
                {
                    'key': 'index-000005',
                    'doc_count': 184464,
                    'max_ts': {'value': 1575463337966.0, 'value_as_string': '2019-12-04T12:42:17.966Z'},
                    'min_ts': {'value': 1575376335698.0, 'value_as_string': '2019-12-03T12:32:15.698Z'},
                },
                {
                    'key': 'index-000004',
                    'doc_count': 175988,
                    'max_ts': {'value': 1575376342679.0, 'value_as_string': '2019-12-03T12:32:22.679Z'},
                    'min_ts': {'value': 1575289333416.0, 'value_as_string': '2019-12-02T12:22:13.416Z'},
                },
                {
                    'key': 'index-000003',
                    'doc_count': 169136,
                    'max_ts': {'value': 1575115339253.0, 'value_as_string': '2019-11-30T12:02:19.253Z'},
                    'min_ts': {'value': 1575028332982.0, 'value_as_string': '2019-11-29T11:52:12.982Z'},
                },
                {
                    'key': 'index-000002',
                    'doc_count': 159471,
                    'max_ts': {'value': 1575289336569.0, 'value_as_string': '2019-12-02T12:22:16.569Z'},
                    'min_ts': {'value': 1575202335222.0, 'value_as_string': '2019-12-01T12:12:15.222Z'},
                },
                {
                    'key': 'index-000001',
                    'doc_count': 129676,
                    'max_ts': {'value': 1575202338431.0, 'value_as_string': '2019-12-01T12:12:18.431Z'},
                    'min_ts': {'value': 1575115342163.0, 'value_as_string': '2019-11-30T12:02:22.163Z'},
                },
            ],
        },
    },
}
