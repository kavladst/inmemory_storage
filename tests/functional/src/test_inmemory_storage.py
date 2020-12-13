import time
from typing import Callable


def test_default_operators(get_response: Callable[[str], str]):
    assert get_response('KEYS') == '[]'
    assert get_response('SET key value') == 'OK'
    assert get_response('GET key') == 'value'
    assert get_response('DEL key') == '1'
    assert get_response('GET key') == 'None'


def test_set_ttl(get_response: Callable[[str], str]):
    tll_seconds = 2
    assert get_response(f'SET key value EX {tll_seconds}') == 'OK'
    assert get_response('GET key') == 'value'
    time.sleep(tll_seconds + 2)
    assert get_response('GET key') == 'None'
    assert get_response(f'SET key value PX {tll_seconds * 1000}') == 'OK'
    assert get_response('GET key') == 'value'
    time.sleep(tll_seconds + 2)
    assert get_response('GET key') == 'None'


def test_set_nx_xx(get_response: Callable[[str], str]):
    assert get_response('SET key value XX') == 'None'
    assert get_response('SET key value') == 'OK'
    assert get_response('SET key new_value_1 XX') == 'OK'
    assert get_response('GET key') == 'new_value_1'
    assert get_response('SET key new_value_2 XX') == 'OK'
    assert get_response('GET key') == 'new_value_2'
    assert get_response('DEL key') == '1'
    assert get_response('SET key new_value_2 NX') == 'OK'
    assert get_response('GET key') == 'new_value_2'
    assert get_response('DEL key') == '1'


def test_hash_operators(get_response: Callable[[str], str]):
    assert get_response('HSET key field_1 value_1 field_2 value_2') == '2'
    assert get_response('HGET key field_1') == 'value_1'
    assert get_response('HGET key field_2') == 'value_2'
    assert get_response('DEL key') == '1'


def test_list_operators(get_response: Callable[[str], str]):
    assert get_response('RPUSH key value_0 value_1 value_2') == '3'
    assert get_response('RPUSH key value_3 value_4 value_5') == '6'
    for i in range(6):
        assert get_response(f'LGET key {i}') == f'value_{i}'
    index_error_msg = 'Index out of range'
    assert get_response('LGET key 10') == index_error_msg
    assert get_response('LGET key -10') == index_error_msg
    assert get_response('LSET key 0 new_value_0') == 'OK'
    assert get_response('LGET key 0') == 'new_value_0'
    assert get_response('SET key_1 value') == 'OK'
    type_key_error_msg = 'Key hold the wrong kind of value'
    assert get_response('RPUSH key_1 value_0') == type_key_error_msg
    assert get_response('DEL key key_1') == '2'
