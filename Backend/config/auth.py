from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required, get_jwt
from flask_restx import Resource, fields, marshal_with
from config.mainConfig import Server
from modules.database.DB import GetUser, GetRevokedTokens
from flask import request

app = Server().GetApp()

jwt = Server().GetJWT()

ns = Server().GetApi().namespace('auth', description='Authentication related operations')

logout_form = ns.model('LogoutForm', {
    'access_token': fields.String(required=True, description='The user\'s refresh token')
})

refresh_response = ns.model('RefreshResponce', {
    'access_token': fields.String(required=True, description='The user\'s new access token')
})

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']



@ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    @ns.doc(responses={
    200: 'access_token',
    401: 'message: Token has expired or is invalid',
    422: 'message: Invalid token or wrong token type',
    401: 'message: Token has been revoked',
    400: 'message: Missing Authorization Header'
})
    @ns.doc(security="ServerAuth")
    @ns.marshal_with(refresh_response)
    def get(self):
        """
        Refresh a user's access token via user's refresh token.
            this should be called when a request fails because the token has expired.
            if this fails then the user should reloggin
            returns a new access token
            header : Authorization : Bearer <refresh_token>
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}, 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in Server().GetBlacklist()

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return GetUser(identity)

@ns.route('/logout')
class Logout(Resource):
    @jwt_required(refresh=True)
    @ns.doc(responses={
    200: 'message: Successfully logged out',
    401: 'message: Token has expired or is invalid',
    422: 'message: Invalid token or wrong token type',
    401: 'message: Token has been revoked',
    400: 'message: Missing Authorization Header'
})
    @ns.doc(security="ServerAuth")
    @ns.expect(logout_form)
    def post(self):
        """
        Logout a user.

            this should be called when a user wants to logout
            it will add the token to the blacklist
            you should pass the access token as well
            header : Authorization : Bearer <refresh_token>
        """
        try:
            jti = get_jwt()['jti']
            Server().AddToBlacklist(jti)
            access_token = request.json['access_token']
            Server().AddToBlacklist(access_token)
        except Exception as e:
            return {'message': 'Invalid token'}, 422
        return {'message': 'Successfully logged out'}, 200