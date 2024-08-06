from flask_restx import Resource, reqparse, fields
from modules.session_management.password import hash_password, verify_password
from config.mainConfig import Server
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, get_jwt, create_refresh_token
from modules.database.DB import GetUser, AddUser, AddRevokedToken
from os import getenv
import traceback
import re

ns = Server().GetApi().namespace('auth', description='Authentication related operations')

login_form = ns.model('LoginForm', {
    'username': fields.String(required=True, description='The user\'s email', default="example@gmail.com"),
    'password': fields.String(required=True, description='The user\'s password')
})

login_responce = ns.model('LoginResponce', {
    'access_token': fields.String(required=True, description='The user\'s JWT token'),
    'refresh_token': fields.String(required=True, description='The user\'s JWT refresh token')
})

register_form = ns.model('RegisterForm', {
    'name': fields.String(required=True, description='The user\'s name'),
    'username': fields.String(required=True, description='The user\'s username'),
    'email': fields.String(required=True, description='The user\'s email', default="example@gmail.com"),
    'password': fields.String(required=True, description='The user\'s password')
})

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' # should be replaced with a library

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_form)
    @ns.doc(responses={403: 'message : Invalid Credentials', 200: 'token', 400: 'message : json args are not valid'})
    @ns.doc(security=None)
    @ns.marshal_with(login_responce)
    def post(self):
        """Login a user.

        This method logs in a user by checking the credentials against the database.
        If the credentials are valid, a JWS token is created and returned to the user.
        This uses email and password as credentials.

        Returns:
            str: The JWS token if the credentials are valid, an error message otherwise.
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', required=True, type=str)
            parser.add_argument('password', required=True , type=str)
            data = parser.parse_args()
            username = data['username']
            password = data['password']
            user = GetUser(username)
            if user:
                if verify_password(password, user['password']):
                    token = create_access_token(identity=user, fresh=True)
                    refresh_token = create_refresh_token(identity=user)
                    return {'access_token': token, 'refresh_token': refresh_token}, 200, {"Content-Type": "application/json"}
                else:
                    return {'message': 'Invalid Credentials'}, 403, {"Content-Type": "application/json"}
            else:
                return {'message': 'Invalid Credentials'}, 403, {"Content-Type": "application/json"}
        except Exception as e:
            if getenv("MODE") == "DEV":
                traceback.print_exc()
                print(e)
            return {'message': 'Invalid Credentials'}, 403, {"Content-Type": "application/json"}

    @ns.doc(responses={403: 'message : Invalid Credentials', 200: 'message : User is authenticated'})
    @ns.doc(security='ServerAuth')
    @jwt_required()
    def get(self):
        """Check if a user is authenticated.

        This method checks if a user is authenticated by checking the validity of the JWS token.
        If the token is valid, the user is authenticated.\n
        NOTE:
        The idea is to call this endpoint before trying to
        login so the user doesn't have to login again.

        Returns:
            str: A success message(code 200) if the user is authenticated,
            an error message otherwise(code 403).
        """
        return {'message': 'User is authenticated'}, 200, {"Content-Type": "application/json"}


@ns.route('/register')
class Register(Resource):
    @ns.expect(register_form)
    @ns.doc(responses={403: 'User already exists', 201: 'token', 400: 'message : json args are not valid'})
    @ns.doc(security=None)
    @ns.marshal_with(login_responce, code=201)
    def post(self):
        """Register a user.

        This method registers a user by adding the user to the database.
        This uses name, surname, email and password as credentials.

        Returns:
            str: A success message if the user was added to the database, an error message otherwise.
        """
        # FIY: this should be refactored when the smtp server is ready
        #   User Registration:
        #     When a user registers, create a unique identifier (e.g., a UUID) for the pending registration.
        #     Store the user's registration details along with the unique identifier in a database table for pending registrations.
        #     Send an email to the user containing a link with the unique identifier (e.g., a link like https://example.com/activate?id=unique_identifier).

        #   Activation Link:
        #     When the user clicks the activation link, your server receives a GET request with the unique identifier as a parameter.
        #     Retrieve the user details from the pending registrations table based on the unique identifier.
        #     If the user is found and the registration is still valid (e.g., within a certain time limit), activate the account by moving the user to the main user table or updating their status.

        #  Login:
        #     Once the account is activated, users can log in using their credentials.
        #  if the user does not do that in 1 hour delete the entry from the database
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', required=True, type=str)
            parser.add_argument('username', required=True, type=str)
            parser.add_argument('email', required=True, type=str)
            parser.add_argument('password', required=True, type=str)
            data = parser.parse_args()
            name = data['name']
            username = data['username']
            email = data['email']
            password = hash_password(data['password'])
            if not re.fullmatch(email_regex, email):
                return {'message': 'json args are not valid'}, 400, {"Content-Type": "application/json"}
            user = AddUser(name, username, email, password)
            if user:
                token = create_access_token(identity=user, fresh=True)
                refresh_token = create_refresh_token(identity=user)
                return {'access_token': token, 'refresh_token': refresh_token}, 201 , {"Content-Type": "application/json"}
            else:
                return {'message': 'User already exists'}, 403, {"Content-Type": "application/json"}
        except Exception as e:
            if getenv("MODE") == "DEV":
                traceback.print_exc()
                print(e)
            return {'message': 'User already exists'}, 403, {"Content-Type": "application/json"}
