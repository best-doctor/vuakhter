scan_response = {
    'took': 9,
    'timed_out': False,
    '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
    'hits': {
        'total': {'value': 10000, 'relation': 'gte'},
        'max_score': 0.0,
        'hits': [
            {
                '_index': 'index',
                '_type': '_doc',
                '_id': 'xxxyyy',
                '_score': 0.0,
                '_source': {
                    'url': {'original': '/prefix/endpoint'},
                    'tags': ['beats_input_codec_plain_applied'],
                    '@timestamp': '2020-05-14T01:41:08.000Z',
                    'input': {'type': 'log'},
                    'fileset': {'name': 'access'},
                    'http': {
                        'request': {'method': 'POST'},
                        'response': {'body': {'bytes': '185'}, 'status_code': '301'},
                    },
                    '@version': '1',
                    'read_timestamp': '2020-05-14T01:41:10.500Z',
                    'host': {'name': 'host-1'},
                    'nginx': {
                        'access': {
                            'remote_ip': '1.2.3.4',
                            'duration': '0.000',
                            'request_id': 'reguest_id_1',
                            'host': '127.0.0.1',
                            'http_version': '1.1',
                        },
                    },
                    'service': {'type': 'nginx'},
                }
            },
        ],
    },
}
