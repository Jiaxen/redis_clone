import time

from app.redis_service import RedisService

def test_ping():
    cache = {}
    rs = RedisService(cache)
    response = rs.handle_request(b"PING\r\n")
    assert response == b"+PONG\r\n"

def test_array_ping():
    cache = {}
    rs = RedisService(cache)
    response = rs.handle_request(b'*1\r\n$4\r\nPING\r\n')
    assert response == b"+PONG\r\n"

def test_echo():
    cache = {}
    rs = RedisService(cache)
    response = rs.handle_request(b'*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n')
    assert response == b'+hey\r\n'

def test_set_and_get():
    cache = {}
    rs = RedisService(cache)
    set_response = rs.handle_request(b'*3\r\n$3\r\nSET\r\n$7\r\nGandalf\r\n$6\r\nWizard\r\n')
    assert set_response == b'+OK\r\n'

    get_response = rs.handle_request(b'*2\r\n$3\r\nGET\r\n$7\r\nGandalf\r\n')
    assert get_response == b'$6\r\nWizard\r\n'

    get_response = rs.handle_request(b'*2\r\n$3\r\nGET\r\n$5\r\nFrodo\r\n')
    assert get_response == b'+-1\r\n'

def test_timed_set_and_get():
    cache = {}
    rs = RedisService(cache)
    set_response = rs.handle_request(b'*5\r\n$3\r\nSET\r\n$5\r\nFrodo\r\n$6\r\nHobbit\r\n$2\r\nPX\r\n$4\r\n1000\r\n')
    assert set_response == b'+OK\r\n'

    get_response = rs.handle_request(b'*2\r\n$3\r\nGET\r\n$5\r\nFrodo\r\n')
    assert get_response == b'$6\r\nHobbit\r\n'
    time.sleep(2)
    get_response = rs.handle_request(b'*2\r\n$3\r\nGET\r\n$5\r\nFrodo\r\n')
    assert get_response == b'+-1\r\n'

