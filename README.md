# Vuakhter

[![Build Status](https://travis-ci.org/best-doctor/vuakhter.svg?branch=master)](https://travis-ci.org/best-doctor/vuakhter)
[![Maintainability](https://api.codeclimate.com/v1/badges/127bff178b6e355fc24c/maintainability)](https://codeclimate.com/github/best-doctor/vuakhter/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/127bff178b6e355fc24c/test_coverage)](https://codeclimate.com/github/best-doctor/vuakhter/test_coverage)

Vuakhter is validation tool to test API to conform our
[API guide](https://github.com/best-doctor/guides/blob/master/guides/api_guide.md).
But it can be used to generate statistics of web-application by its logs.

## Principles of work

Vuakhter scans access log for specified period, filters log entries by path prefixes
and passes each entry for statistics generation.

Base class `AccessLog` returns an iterator of log entries. Class `ElasticAccessLog`
scans elastic indices for log entries.

`StatisticsMetrics` gets `AccessEntry` records and forms array of statistics data.
`StatisticsMetrics.report() -> str` returns statistics report for the metrics.

`HttpAnalyzer` uses `access_log: AccessLog` and array of `StatisticsMetrics`.

Only one metric `SchemaValidatorCounter` is passing to `HttpAnalyzer` in main script
`vuakhter`. It uses `request_log: RequestLog` to validate API responses.

Class `ElasticRequestLog: RequestLog` scans elastic indices requests by request_id
 and returns array of `RequestEntry`. `SchemaValidatorCounter` checks all responses
 bodies and counts valid API calls.

## Usage

```
vuakhter [--es-user ES_USER] [--es-pass ES_PASS] [--es-host ES_HOST] [--es-port ES_PORT
[--start-date START_DATE] [--end-date END_DATE] prefixes [prefixes ...]
```

By default end_date is current date and time if not specified. And start_date
defaults to day ago end_date.

All connection parameters may be specified in .env file.

```
ES_USER=elastic ES_PASS=pasword ES_HOST=localhost vuakhter /api/

```

### Using in code

```python
import datetime

from elasticsearch import Elasticsearch

from vuakhter.analyzer import HttpAnalyzer
from vuakhter.kibana.access_log import ElasticAccessLog
from vuakhter.metrics.counters import ComplexCounter


elastic = Elasticsearch()
access_log = ElasticAccessLog(index_pattern='filebeat-*', client=elastic)

http_analyzer = HttpAnalyzer(access_log=access_log)
http_analyzer.add_metrics(ComplexCounter())

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=1)

http_analyzer.analyze(start_date, end_date)

for metric in http_analyzer.metrics:
    metric.finalize()
    print(metric.report())
```
