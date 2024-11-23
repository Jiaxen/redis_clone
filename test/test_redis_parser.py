import pytest

from app.redis_parser import RedisParser

def test_decode_simple_redis_array():
    rp = RedisParser()
    res = rp.decode(b"*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n")
    assert res == ["ECHO", "hey"]

def test_decode_long_redis_array():
    rp = RedisParser()
    res = rp.decode(b"*5\r\n$3\r\nSET\r\n$4\r\nPING\r\n$4\r\nPONG\r\n$2\r\nPX\r\n$4\r\n1000\r\n")
    assert res == ["SET", "PING", "PONG", "PX", "1000"]

def test_decode_malformed_array():
    rp = RedisParser()
    with pytest.raises(ValueError):
        rp.decode(b"*2\r\n$5\r\nECHO\r\n$3\r\nhey\r\n")
