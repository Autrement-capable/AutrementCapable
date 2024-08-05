from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from modules.utils.singleton import singleton
from datetime import timedelta
# from modules.database.create_db import *


app_name = "Autrement Capable"

authorization_header = {
    'ServerAuth' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'The JWT token to authenticate the user. Format: "Bearer {token}"'
    }
}


@singleton
class Server():
    def __init__(self) -> None:
        """Initialize the Flask app and the Flask-RESTPlusx API."""
        load_dotenv()
        self.app = Flask(__name__)

        self.app.config['JWT_SECRET_KEY'] = getenv('SERVER_SECRET')

        # this the things that we accept as a carrier of the token
        self.app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]

        # in production we should set this to True so that the token is only sent over https
        self.app.config["JWT_COOKIE_SECURE"] = False if getenv("MODE") == "DEV" else True

        self.app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

        self.app.config["DEBUG"] = True if getenv("MODE") == "DEV" else False

        self.jwt = JWTManager(self.app)

        CORS(self.app, supports_credentials=True, allow_headers="*", origins="http://localhost")

        self.api = Api(app=self.app, version=getenv("VERSION"), title="Autrement Capable API Dev Server",
                       description="The API for the DrumGan project Monetization.",
                       doc="/docs" if self.app.config["DEBUG"] else False, prefix="",
                       authorizations=[authorization_header], default="Global",
                       default_label="Base", default_swagger_filename="Docs.json",
                       validate=True)

        self.port = getenv('PORT') if getenv('PORT') else 5000

    def Run(self) -> None:
        """Run the Flask app.

        This method starts the Flask application.

        Returns:
            None
        """
        self.app.run(port=self.port, host='0.0.0.0', debug=self.app.config["DEBUG"])

    def AddResource(self, resource, route) -> None:
        """Add a resource to the Flask-RESTPlus API.

        Args:
            resource: The resource to add. (class Resource)
            route (str): The route to add the resource to.

        Returns:
            None
        """
        self.api.add_resource(resource, route)

    def GetApp(self) -> Flask:
        """Get the Flask app.

        Returns:
            Flask: The Flask app.
        """
        return self.app

    def GetApi(self) -> Api:
        """Get the Flask-RESTPlus API.

        Returns:
            Api: The Flask-RESTPlus API.
        """
        return self.api

    def GetJWT(self) -> JWTManager:
        """Get the JWTManager.

        Returns:
            JWTManager: The JWTManager.
        """
        return self.jwt

__all__ = ['Server']
