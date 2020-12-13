from flask_restplus import Namespace, Resource, reqparse

from models.storage.storage import UsersStorage
from models.storage.exceptions import UserNotFound

users_storage = UsersStorage()

api_user_storage = Namespace('user_storage')

params_user_id_parser = reqparse.RequestParser()
params_user_id_parser.add_argument('user_id', required=True)

params_get_parser = params_user_id_parser.copy()
params_get_parser.add_argument('key', required=True)

params_hash_get_parser = params_get_parser.copy()
params_hash_get_parser.add_argument('field', required=True)

params_list_get_parser = params_get_parser.copy()
params_list_get_parser.add_argument('index', required=True, type=int)

params_set_parser = params_get_parser.copy()
params_set_parser.add_argument('value', required=True)
params_set_parser.add_argument('nx', type=bool)
params_set_parser.add_argument('xx', type=bool)
params_set_parser.add_argument('ttl', type=float)

params_hash_set_parser = params_get_parser.copy()
params_hash_set_parser.add_argument('fields', required=True, action='split')
params_hash_set_parser.add_argument('values', required=True, action='split')

params_list_set_parser = params_list_get_parser.copy()
params_list_set_parser.add_argument('value', required=True)

params_delete_parser = params_user_id_parser.copy()
params_delete_parser.add_argument('keys', required=True, action='split')

params_rpush_parser = params_get_parser.copy()
params_rpush_parser.add_argument('values', required=True, action='split')


@api_user_storage.route('/get')
@api_user_storage.doc(parser=params_get_parser)
class ValueGetStorage(Resource):

    def get(self):
        args = params_get_parser.parse_args()
        user_id = args['user_id']
        key = args['key']

        try:
            value = users_storage.get_value(key, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404
        return {'response': value}


@api_user_storage.route('/hash_get')
@api_user_storage.doc(parser=params_hash_get_parser)
class HashGetStorage(Resource):

    def get(self):
        args = params_hash_get_parser.parse_args()
        user_id = args['user_id']
        key = args['key']
        field = args['field']

        try:
            value = users_storage.get_value(key, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404

        if not isinstance(value, dict):
            return {'error': 'Key hold the wrong kind of value'}
        return {'response': value.get(field)}


@api_user_storage.route('/list_get')
@api_user_storage.doc(parser=params_list_get_parser)
class ListGetStorage(Resource):

    def get(self):
        args = params_list_get_parser.parse_args()
        user_id = args['user_id']
        key = args['key']
        index = args['index']

        try:
            data = users_storage.get_value(key, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404

        if not isinstance(data, list):
            return {'error': 'Key hold the wrong kind of value'}
        if index < 0 or len(data) <= index:
            return {'error': 'Index out of range'}
        return {'response': data[index]}


@api_user_storage.route('/set')
@api_user_storage.doc(parser=params_set_parser)
class ValueSetStorage(Resource):

    def post(self):
        args = params_set_parser.parse_args()
        user_id = args['user_id']
        key = args['key']
        value = args['value']
        nx = args.get('nx', False)
        xx = args.get('xx', False)
        ttl = args.get('ttl')

        try:
            response = users_storage.set_value(
                key, value, user_id, nx=nx, xx=xx, ttl=ttl
            )
        except UserNotFound as e:
            return {'error': str(e)}, 404
        return {'response': None if response is None else 'OK'}


@api_user_storage.route('/hash_set')
@api_user_storage.doc(parser=params_hash_set_parser)
class HashSetStorage(Resource):

    def post(self):
        args = params_hash_set_parser.parse_args()
        user_id = args['user_id']
        key = args['key']
        fields = args['fields']
        values = args['values']
        if len(values) != len(fields):
            return {'error': 'Count values and count fields must be equal'}
        new_dictionary = dict(zip(fields, values))
        try:
            dictionary = users_storage.get_value(key, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404

        if not dictionary:
            users_storage.set_value(key, new_dictionary, user_id)
            return {'response': len(new_dictionary)}
        if not isinstance(dictionary, dict):
            return {'error': 'Key hold the wrong kind of value'}
        count_new_elements = len(set(new_dictionary) - set(dictionary))
        dictionary.update(new_dictionary)
        return {'response': count_new_elements}


@api_user_storage.route('/list_set')
@api_user_storage.doc(parser=params_list_set_parser)
class ListSetStorage(Resource):

    def post(self):
        args = params_list_set_parser.parse_args()
        user_id = args['user_id']
        key = args['key']
        index = args['index']
        new_value = args['value']

        try:
            data = users_storage.get_value(key, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404

        if not isinstance(data, list):
            return {'error': 'Key hold the wrong kind of value'}
        if index < 0 or len(data) <= index:
            return {'error': 'Index out of range'}
        data[index] = new_value
        return {'response': 'OK'}


@api_user_storage.route('/rpush')
@api_user_storage.doc(parser=params_rpush_parser)
class RPushValuesStorage(Resource):

    def post(self):
        args = params_rpush_parser.parse_args()
        user_id = args['user_id']
        key = args['key']
        values = args['values']
        try:
            data = users_storage.get_value(key, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404
        if data is None:
            data = values
            users_storage.set_value(
                key, data, user_id
            )
        elif isinstance(data, list):
            data += values
        else:
            return {'error': 'Key hold the wrong kind of value'}
        return {'response': len(data)}


@api_user_storage.route('/delete')
@api_user_storage.doc(parser=params_delete_parser)
class DeleteValueStorage(Resource):

    def delete(self):
        args = params_delete_parser.parse_args()
        user_id = args['user_id']
        keys = args['keys']

        try:
            count_deleted_elements = users_storage.delete_values(keys, user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404
        return {'response': count_deleted_elements}


@api_user_storage.route('/keys')
@api_user_storage.doc(parser=params_user_id_parser)
class GetKeysStorage(Resource):

    def get(self):
        args = params_user_id_parser.parse_args()
        user_id = args['user_id']

        try:
            keys = users_storage.get_keys(user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404
        return {'response': keys}


@api_user_storage.route('/save')
@api_user_storage.doc(parser=params_user_id_parser)
class SaveStorage(Resource):

    def post(self):
        args = params_user_id_parser.parse_args()
        user_id = args['user_id']

        try:
            users_storage.save_data(user_id)
        except UserNotFound as e:
            return {'error': str(e)}, 404
        return {'response': 'OK'}
