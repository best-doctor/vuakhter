from vuakhter.metrics.base import StatisticsMetrics


def test_statistics_metrics():
    instance = StatisticsMetrics()

    instance.statistics['name'] = 10
    assert instance.report() == 'Some metrics\n------------\nname 10'
