from __future__ import annotations
import datetime
import os

from elasticsearch import Elasticsearch

from vuakhter.analyzer import AccessLogAnalyzer
from vuakhter.kibana.access_log import ElasticAccessLog
from vuakhter.kibana.requests_log import ElasticRequestsLog
from vuakhter.metrics.counters import SchemaValidatorCounter, SlowLogCounter, ComplexCounter


def main() -> None:
    import argparse
    from vuakhter.utils.helpers import setup_logging

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    parser.add_argument('--es-user', default=os.environ.get('ES_USER'))
    parser.add_argument('--es-pass', default=os.environ.get('ES_PASS'))
    parser.add_argument('--es-host', default=os.environ.get('ES_HOST'))
    parser.add_argument('--es-port', type=int, default=9243)

    parser.add_argument('--start-date', type=datetime.datetime.fromisoformat, default=None)
    parser.add_argument('--end-date', type=datetime.datetime.fromisoformat, default=None)
    parser.add_argument('prefixes', default='/api/', type=str, nargs='+')

    args = parser.parse_args()

    if args.debug:
        setup_logging(level='DEBUG', formatter='verbose')
    elif args.verbose:
        setup_logging(level='INFO', formatter='verbose')
    else:
        setup_logging()

    client = Elasticsearch(http_auth=(args.es_user, args.es_pass), host=args.es_host, port=args.es_port, use_ssl=True)
    access_log = ElasticAccessLog('filebeat-*', client=client)
    requests_log = ElasticRequestsLog('django-*', client=client)
    analyzer = AccessLogAnalyzer(access_log)

    analyzer.add_metric(SchemaValidatorCounter(requests_log))
    analyzer.add_metric(SlowLogCounter(top=10, mangle=False))
    analyzer.add_metric(ComplexCounter())

    end_date = args.end_date or datetime.datetime.now()
    start_date = args.start_date or end_date - datetime.timedelta(days=1)

    analyzer.analyze(start_date, end_date, prefixes=(args.prefixes or ['/']))

    for metric in analyzer.metrics:
        metric.finalize()
        print(metric.report())  # noqa: T001


if __name__ == '__main__':
    main()
