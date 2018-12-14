import pytest
from datetime import datetime, timezone, timedelta


@pytest.mark.parametrize("string,delim,output", [
    (" ", " ", ("", "")),
    ("token ", " ", ("token", "")),
    ("token other tokens", " ", ("token", "other tokens")),
    ("quoted token\" other tokens", "\"", ("quoted token", " other tokens")),
    ("escaped\\ token ", " ", ("escaped token", "")),
])
def test_parse_string(httpmonitor, string, delim, output):
    assert output == httpmonitor.parse_string(string, delim)


@pytest.mark.parametrize("string,delim", [
    ("", " "),
    ("token", " "),
    ("escaped\\ token", " "),
])
def test_parse_string_failure(httpmonitor, string, delim):
    with pytest.raises(ValueError):
        httpmonitor.parse_string(string, delim)


@pytest.mark.parametrize("string,output", [
    ("14/Dec/2018:02:00:22 +0000",
     datetime(2018, 12, 14, 2, 0, 22, 0, timezone.utc)),
    ("09/May/2018:16:00:39 +0000",
     datetime(2018, 5, 9, 16, 0, 39, 0, timezone.utc)),
    ("09/May/2018:16:00:39 +0100",
     datetime(2018, 5, 9, 16, 0, 39, 0, timezone(timedelta(hours=1)))),
])
def test_parse_datetime(httpmonitor, string, output):
    assert output == httpmonitor.parse_datetime(string)


@pytest.mark.parametrize("string", [
    "09/Bla/2018:16:00:39 +0000",
    "30/Feb/2018:16:00:39 +0000",
    "30/May/2018:16:00 +0000",
    "30/May/2018:16:00:49",
    "really not a date"])
def test_parse_datetime_failure(httpmonitor, string):
    with pytest.raises(ValueError):
        httpmonitor.parse_datetime(string)


@pytest.mark.parametrize("string,method,uri,protocol", [
    ("GET / HTTP/1.0", "GET", "/", "HTTP/1.0"),
    ("GET / HTTP/1.1", "GET", "/", "HTTP/1.1"),
    ("GET / HTTP/2.0", "GET", "/", "HTTP/2.0"),
    ("get / HTTP/1.0", "GET", "/", "HTTP/1.0"),
    ("HEAD / HTTP/1.0", "HEAD", "/", "HTTP/1.0"),
    ("OPTIONS / HTTP/1.0", "OPTIONS", "/", "HTTP/1.0"),
    ("GET /something HTTP/1.1", "GET", "/something", "HTTP/1.1"),
    ("GET /something%20else HTTP/1.1", "GET", "/something%20else", "HTTP/1.1"),
    ("GET /something?arg=1 HTTP/1.1", "GET", "/something?arg=1", "HTTP/1.1"),
])
def test_parse_request(httpmonitor, string, method, uri, protocol):
    assert httpmonitor.parse_request(string) == dict(method=method,
                                                     uri=uri,
                                                     protocol=protocol)


@pytest.mark.parametrize("string", [
    "GET /",
    "GET / / HTTP/1.0",
    "GET HTTP/1.0",
    "GET / HTTP/3.0",
])
def test_parse_request_failure(httpmonitor, string):
    with pytest.raises(ValueError):
        httpmonitor.parse_request(string)


@pytest.mark.parametrize("string,expected", [
    ('127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
     '"GET /report HTTP/1.0" 200 123',
     dict(ip="127.0.0.1",
          user="-",
          auth="james",
          date=datetime(2018, 5, 9, 16, 0, 39, 0, timezone.utc),
          request=dict(method="GET",
                       uri="/report",
                       protocol="HTTP/1.0"),
          status=200,
          size=123)),
    ('2001:db8::1.1.1.1 - - [09/May/2018:16:00:39 +0000] '
     '"HEAD /report HTTP/1.0" 200 0',
     dict(ip="2001:db8::1.1.1.1",
          user="-",
          auth="-",
          date=datetime(2018, 5, 9, 16, 0, 39, 0, timezone.utc),
          request=dict(method="HEAD",
                       uri="/report",
                       protocol="HTTP/1.0"),
          status=200,
          size=0)),
])
def test_parse_logline(httpmonitor, string, expected):
    assert expected == httpmonitor.parse_logline(string)


@pytest.mark.parametrize("string", [
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" 200',
    '127.0.0.1 james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" 200 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/3.0" 200 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" 600 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" 200 -16',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" 200 123 88',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000]'
    '"GET /report HTTP/1.0" 200 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000 '
    '"GET /report HTTP/1.0" 200 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0 200 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" aaa 123',
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
    '"GET /report HTTP/1.0" 200 bbb',
])
def test_parse_logline_failure(httpmonitor, string):
    with pytest.raises(ValueError):
        httpmonitor.parse_logline(string)

