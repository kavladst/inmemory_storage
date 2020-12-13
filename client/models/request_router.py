from typing import Optional, List

import requests
from requests.models import Response

from core.config import API_URL
from core import consts


class RequestRouter:

    def __init__(self):
        self._user_id: Optional[str] = None

    def route_request(self, request: str) -> str:
        splitted_request: List[str] = request.split(' ')
        method, params_list = splitted_request[0], splitted_request[1:]
        if method not in consts.ALL_METHODS:
            return 'Method not allowed'

        if ((method not in (consts.LOGIN, consts.REGISTER)) and
                self._user_id is None):
            return 'You need to login'
        if method == consts.LOGOUT:
            if params_list:
                return 'Wrong number of arguments'
            self._user_id = None
            return 'OK'

        params = self._get_parsed_params_by_method(method, params_list)
        if params is None:
            return 'Wrong number of arguments'

        params['user_id'] = self._user_id
        response = self._get_response_for_request(method, params)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return str(e)
        response_data = response.json()
        if 'response' in response_data:
            if method == consts.LOGIN or method == consts.REGISTER:
                self._user_id = response_data['login']
            return str(response_data['response'])
        return str(response_data['error'])

    @staticmethod
    def _get_parsed_params_by_method(method: str, params_list: List[str]
                                     ) -> Optional[dict]:
        params = None
        if method == consts.LOGIN or method == consts.REGISTER:
            if len(params_list) != 2:
                return
            params = {'login': params_list[0], 'password': params_list[1]}
        elif method == consts.GET:
            if len(params_list) != 1:
                return
            params = {'key': params_list[0]}
        elif method == consts.HGET:
            if len(params_list) != 2:
                return
            params = {'key': params_list[0], 'field': params_list[1]}
        elif method == consts.LGET:
            if len(params_list) != 2:
                return
            params = {'key': params_list[0], 'index': params_list[1]}
        elif method == consts.SET:
            params = {}
            for attr in ('nx', 'xx'):
                if attr.upper() in params_list:
                    params[attr] = True
                    params_list.remove(attr.upper())
            if len(params_list) == 4:
                if params_list[2] == 'EX' and params_list[3].isnumeric():
                    params['ttl'] = int(params_list[3])
                elif params_list[2] == 'PX' and params_list[3].isnumeric():
                    params['ttl'] = int(params_list[3]) / 1000
                else:
                    return
                params_list = params_list[0: 2]
            if len(params_list) != 2:
                return
            params['key'] = params_list[0]
            params['value'] = params_list[1]
        elif method == consts.HSET:
            if len(params_list) < 3 and len(params_list) % 2 == 0:
                return
            params = {
                'key': params_list[0],
                'fields': ','.join(
                    params_list[i] for i in range(1, len(params_list), 2)
                ), 'values': ','.join(
                    params_list[i] for i in range(2, len(params_list), 2)
                )
            }
        elif method == consts.LSET:
            if len(params_list) != 3:
                return
            params = {
                'key': params_list[0],
                'index': params_list[1],
                'value': params_list[2],
            }
        elif method == consts.DEL:
            if len(params_list) == 0:
                return
            params = {'keys': ','.join(params_list)}
        elif method == consts.KEYS:
            if len(params_list):
                return
            params = {}
        elif method == consts.RPUSH:
            if len(params_list) < 2:
                return
            params = {
                'key': params_list[0],
                'values': ','.join(
                    (params_list[i] for i in range(1, len(params_list)))
                )
            }
        elif method == consts.SAVE:
            if len(params_list):
                return
            params = {}
        return params

    @staticmethod
    def _get_response_for_request(method: str, params: dict) -> Response:
        request_type = consts.REQUEST_TYPE_FOR_METHODS[method]
        if request_type == consts.GET_REQUEST_TYPE:
            return requests.get(
                f'{API_URL}{consts.ROUTE_FOR_METHODS[method]}',
                params=params
            )
        elif request_type == consts.POST_REQUEST_TYPE:
            return requests.post(
                f'{API_URL}{consts.ROUTE_FOR_METHODS[method]}',
                params=params
            )
        elif request_type == consts.DELETE_REQUEST_TYPE:
            return requests.delete(
                f'{API_URL}{consts.ROUTE_FOR_METHODS[method]}',
                params=params
            )
