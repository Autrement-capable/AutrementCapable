from mongoengine import connect, Document, IntField, StringField, BooleanField, ObjectIdField
from pymongo import MongoClient
from bson import ObjectId

class User(Document):
    name = StringField(required=True)
    surname = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    subscribed = BooleanField()
    stripeCustomerId = StringField()
    tokens = IntField()

class CheckoutProduct(Document):
    name = StringField(required=True)
    price_id = StringField(required=True)
    description = StringField(required=True)

class Subscription(Document):
    name = StringField(required=True)
    price_id = StringField(required=True)
    description = StringField(required=True)

class Service(Document):
    name = StringField(required=True)
    priceOriginal = IntField(required=True)
    pricePremium = IntField(required=True)
    description = StringField(required=True)

class RevokedToken(Document):
    pass

def initialize_database(mongo_host: str, mongo_port: int, database_name: str):
    try:
        # Connect to MongoDB server using mongoengine
        connect(db=database_name, host=mongo_host, port=mongo_port)

        # Return the client and collections
        return User, Service, CheckoutProduct, Subscription, RevokedToken

    except Exception as e:
        print(e)
        return None, None, None, None, None
    

def AddService( name: str, priceOriginal: int, pricePremium: int, description: str) -> bool:
    """Add a service to the database.

    Args:
        name (str): The service's name.
        priceOriginal (int): The service's price for original users.
        pricePremium (int): The service's price for premium users.
        description (str): The service's description.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        Services_collection = Service._get_collection()
        if Services_collection.find_one({'name': name}) is None:
            Services_collection.insert_one({
                'name': name,
                'priceOriginal': priceOriginal,
                'pricePremium': pricePremium,
                'description': description
            })
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    

def AddUser(users_collection, name: str, surname: str, email: str, password: str) -> bool:
    try:
        if users_collection.find_one({'email': email}) is None:
            users_collection.insert_one({
                'name': name,
                'surname': surname,
                'email': email,
                'password': password,
                'subscribed': False,
                'stripeCustomerId': None,
                'tokens': 3
            })
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


# Example usage

# intialize the database
client = MongoClient("mongodb://localhost:27017/")
db = client["Another_Monetization_DB"]

User, Service, RevokedToken, CheckoutProduct, Subscription = initialize_database('localhost', 27017, 'Another_Monetization_DB')

# Create a new user with a unique identifier
users_collection = User._get_collection()
service_collection = Service._get_collection()

# Add a new user
result = AddService("Service 1", 10, 5, "This is a service that can be used by the user via tokens or subscription")

client1 = MongoClient("mongodb://localhost:27017/")
existing_dbs = client1.list_database_names()

# Get a list of collection names in the database
collection_names = db.list_collection_names()

# Print the collection names
print(f"Collections in the 'Monetization_DB' database: {collection_names}")
#parse through collections and print the documents
for collection in collection_names:
    print(f"Documents in the {collection} collection:")
    for document in db[collection].find():
        print(document)

print(f"Existing databases: {existing_dbs}")