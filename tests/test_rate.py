import pytest


@pytest.mark.parametrize("string,hits,interval", [
    ("1/s", 1, 1),
    ("1/5s", 1, 5),
    ("5/s", 5, 1),
    ("1/m", 1, 60),
    ("10/h", 10, 3600),
    ("100/10m", 100, 600),
])
def test_rate(httpmonitor, string, hits, interval):
    rate = httpmonitor.rate(string)
    assert (rate.hits, rate.interval) == (hits, interval)
