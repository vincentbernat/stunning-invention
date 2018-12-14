import pytest


@pytest.mark.parametrize("string,num,denum", [
    ("1/s", 1, 1),
    ("1/5s", 1, 5),
    ("5/s", 5, 1),
    ("1/m", 1, 60),
    ("10/h", 10, 3600),
    ("100/10m", 100, 600),
])
def test_rate(httpmonitor, string, num, denum):
    assert (num, denum) == httpmonitor.rate(string)
