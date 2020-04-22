# Vuakhter

Vuakhter создавался для валидации API на соответствие нашему
[API guide](https://github.com/best-doctor/guides/blob/master/guides/api_guide.md).
Но может использоваться, например, для формирования статистики по логам web-приложения.

## Принцип работы

Vuakhter выбирает из access log указанный период, фильтрует записи по префиксам, передает каждую запись в массив метрик
для формирования статистики.

Базовый класс `AccessLog` возвращает итератор по записям лога. Его реализация `ElasticAccessLog` выбирает записи из
индексов в elastic.

`StatisticsMetrics` принимает записи `AccessEntry` и формирует массив статистики. `StatisticsMetrics.report() -> str`
возвращает отчет по метрике.

`HttpAnalyzer` принимает на вход `access_log: AccessLog` и массив `StatisticsMetrics`.

В скрипте `vuakhter` в `HttpAnalyzer` добавляется одна метрика - `SchemaValidatorCounter`, которая использует
`request_log: RequestLog` для валидации ответов API.

`RequestLog` и его реализация `ElasticRequestLog` ищет из индексов elastic запрос по request_id и возвращает набор
`RequestEntry`, проверяет тело ответа, собирает количество вызовов API, которые удовлетворяют
[API guide](https://github.com/best-doctor/guides/blob/master/guides/api_guide.md).

## Использование

```
vuakhter [--es-user ES_USER] [--es-pass ES_PASS] [--es-host ES_HOST] [--es-port ES_PORT] [--start-date START_DATE] [--end-date END_DATE] prefixes [prefixes ...]

```

Если end_date не указан, то по умолчанию это текущий
момент времени. Если не указан start_date, то по умолчанию это момент времени за сутки до end_date.

Параметры для коннекта к elastic могут быть переданы через env.

```
ES_USER=elastic ES_PASS=pasword ES_HOST=localhost vuakhter /api/

```

### Использование в коде

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
