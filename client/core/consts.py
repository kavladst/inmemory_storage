GET = 'GET'
HGET = 'HGET'
LGET = 'LGET'
SET = 'SET'
HSET = 'HSET'
LSET = 'LSET'
RPUSH = 'RPUSH'
DEL = 'DEL'
KEYS = 'KEYS'
LOGIN = 'LOGIN'
REGISTER = 'REGISTER'
LOGOUT = 'LOGOUT'
SAVE = 'SAVE'

ALL_METHODS = {
    GET, HGET, LGET,
    SET, HSET, LSET, RPUSH,
    DEL, KEYS, SAVE,
    LOGIN, REGISTER, LOGOUT
}

ROUTE_FOR_METHODS = {
    GET: 'user_storage/get',
    HGET: 'user_storage/hash_get',
    LGET: 'user_storage/list_get',
    SET: 'user_storage/set',
    HSET: 'user_storage/hash_set',
    LSET: 'user_storage/list_set',
    RPUSH: 'user_storage/rpush',
    DEL: 'user_storage/delete',
    KEYS: 'user_storage/keys',
    SAVE: 'user_storage/save',
    LOGIN: 'api_authentification/login',
    REGISTER: 'api_authentification/register'
}

GET_REQUEST_TYPE = 'get'
POST_REQUEST_TYPE = 'post'
DELETE_REQUEST_TYPE = 'delete'

REQUEST_TYPE_FOR_METHODS = {
    GET: GET_REQUEST_TYPE,
    HGET: GET_REQUEST_TYPE,
    LGET: GET_REQUEST_TYPE,
    SET: POST_REQUEST_TYPE,
    HSET: POST_REQUEST_TYPE,
    LSET: POST_REQUEST_TYPE,
    RPUSH: POST_REQUEST_TYPE,
    DEL: DELETE_REQUEST_TYPE,
    KEYS: GET_REQUEST_TYPE,
    SAVE: POST_REQUEST_TYPE,
    LOGIN: GET_REQUEST_TYPE,
    REGISTER: POST_REQUEST_TYPE
}
