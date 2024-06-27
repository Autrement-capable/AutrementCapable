from flask import Flask, jsonify
from flask_restx import Api, Resource
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from pymongo import MongoClient
from modules.utils.singleton import singleton
from modules.database.create_db import *


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
class Config():
    def __init__(self) -> None:
        """Initialize the Flask app and the Flask-RESTPlusx API."""
        load_dotenv()
        self.app = Flask(__name__)
        self.mongo_host = "localhost"
        self.mongo_port = 27017
        self.database_name = "Final_Monetization_DB"
        self.app.config['SECRET_KEY'] = getenv('SERVER_SECRET_KEY_PRIVATE')
        CORS(self.app, supports_credentials=True, allow_headers="*", origins="*")
        self.api = Api(app=self.app, version=getenv("VERSION"), title="DrumGan Monezation API",
                       description="The API for the DrumGan project Monetization.",
                       doc="/docs", authorizations=authorization_header, default="Global",
                       default_label="Global Namespace", default_swagger_filename="Docs.json",
                       validate=True)
        self.port = getenv('PORT') if getenv('PORT') else 5000
        self.client, self.Services_collection, self.users_collection, self.revoked_tokens_collection, self.checkout_products_collection, self.subscriptions_collection = initialize_database(self.mongo_host, self.mongo_port, self.database_name)
        self.collections_info = {
            "Services_collection" : self.Services_collection,
            "users_collection" : self.users_collection,
            "revoked_tokens_collection" : self.revoked_tokens_collection,
            "checkout_products_collection" : self.checkout_products_collection,
            "subscriptions_collection" : self.subscriptions_collection
        }
        if getenv("MODE") == "DEV":
            # testing goes here
            pass

    def Run(self) -> None:
        """Run the Flask app.

        This method starts the Flask application.

        Returns:
            None
        """
        self.app.run(port=self.port, host='0.0.0.0', debug=True if getenv("MODE") == "DEV" else False)

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

    def GetCollections(self) -> dict:
        """Get the database collections.

        Returns:
            dict: The database collections.
        """
        return self.collections_info
