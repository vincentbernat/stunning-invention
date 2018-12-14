import pytest


@pytest.fixture
def meter(httpmonitor):
    return httpmonitor.Meter(10)


@pytest.fixture(params=[0, 2, 3, 7, 9, 13])
def now(request):
    return request.param + 100


def test_empty_meter(meter):
    assert meter.average() == 0


def test_meter_oneupdate(meter, now):
    meter.increase(5, now)
    assert meter.average() == 0.5


def test_meter_severalupdates(meter, now):
    meter.increase(5, now)
    meter.increase(15, now)
    assert meter.average() == 2


def test_meter_severalvalues(meter, now):
    meter.increase(5, now)
    meter.increase(15, now+1)
    assert meter.average() == 2


def test_meter_manyvalues(meter, now):
    for i in range(10):
        meter.increase(5, now + i)
    assert meter.average() == 5


def test_meter_manymorevalues(meter, now):
    for i in range(10):
        meter.increase(5, now + i)
    meter.increase(10, now + 10)
    assert meter.average() == 5.5


def test_meter_skipping_clock(meter, now):
    for i in range(10):
        meter.increase(5, now + i)
    # [5,5,5,5,5,5,5,5,5,5]
    meter.increase(10, now + 15)
    # [0,0,0,0,0,10,5,5,5,5]
    assert meter.average() == 3


def test_invalid_timestamp(meter, now):
    meter.increase(5, now)
    with pytest.raises(ValueError):
        meter.increase(15, now-1)
