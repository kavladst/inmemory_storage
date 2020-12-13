from flask_restplus import Namespace, Resource, reqparse

from api.user_storage import users_storage
from models.authentification.authentification import UserAuthentification

users_auth = UserAuthentification()

api_authentification = Namespace('api_authentification')

user_info_parser = reqparse.RequestParser()
user_info_parser.add_argument('login', required=True)
user_info_parser.add_argument('password', required=True)


@api_authentification.route('/register')
@api_authentification.doc(parser=user_info_parser)
class RegisterAuthentification(Resource):

    def post(self):
        args = user_info_parser.parse_args()
        input_login = args['login']
        input_password = args['password']

        login = users_auth.register_user(input_login, input_password)
        if login is None:
            return {'error': 'login already exists'}
        users_storage.add_user(input_login)
        return {'login': login, 'response': 'OK'}


@api_authentification.route('/login')
@api_authentification.doc(parser=user_info_parser)
class LoginAuthentification(Resource):

    def get(self):
        args = user_info_parser.parse_args()
        input_login = args['login']
        input_password = args['password']

        login = users_auth.login_user(input_login, input_password)
        if login is None:
            return {'error': 'login or password is invalid'}
        return {'login': login, 'response': 'OK'}
