scan_access_response = {
    'took': 9,
    'timed_out': False,
    '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
    'hits': {
        'total': {'value': 10000, 'relation': 'gte'},
        'max_score': 0.0,
        'hits': [
            {
                '_index': 'index-access',
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
                },
            },
        ],
    },
}


scan_requests_response = {
    'took': 346,
    'timed_out': False,
    '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
    'hits': {
        'total': {'value': 435, 'relation': 'eq'},
        'max_score': 0.0,
        'hits': [
            {
                '_index': 'index-requests',
                '_type': '_doc',
                '_id': 'Fg3bFHIBFgzipKveQeIb',
                '_score': 0.0,
                '_source': {
                    'type': 'python',
                    'tags': ['beats_input_codec_plain_applied'],
                    '@timestamp': '2020-05-14T20:23:32.084Z',
                    'pid': 21165,
                    'response': {
                        'type': 'json_response_log',
                        'json': '{"is_enabled": false}',
                        'status': '200',
                        'request_id': 'request_id_1',
                    },
                    'logsource': 'host-1',
                    '@version': '1',
                    'host': 'host-1',
                },
            },
            {
                '_index': 'django-2019-11.28-000143',
                '_type': '_doc',
                '_id': '9Q3cFHIBFgzipKveAuqt',
                '_score': 0.0,
                '_source': {
                    'type': 'python',
                    'tags': ['beats_input_codec_plain_applied'],
                    '@timestamp': '2020-05-14T20:24:20.498Z',
                    'response': {
                        'type': 'json_response_log',
                        'json': '{"data": {}}',
                        'status': '200',
                        'request_id': 'request_id_2',
                    },
                    'logsource': 'host-1',
                    '@version': '1',
                    'host': 'host-1',
                },
            },
        ],
    },
}
