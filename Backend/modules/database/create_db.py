from pymongo import MongoClient
from mongoengine import connect, Document, IntField, StringField, BooleanField, ObjectIdField
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

# Connect to MongoDB server
# Usage
# client, User, Service, RevokedToken, CheckoutProduct, Subscription = initialize_database('localhost', 27017, 'Monetization_DB')
def initialize_database(mongo_host: str, mongo_port: int, database_name: str):
    try:
        # Connect to MongoDB server using mongoengine
        connect(db=database_name, host=mongo_host, port=mongo_port)

        # Connect to MongoDB server using pymongo for the client reference
        client = MongoClient(mongo_host, mongo_port)

        # Get references to the collections
        user_collection = User
        service_collection = Service
        revoked_token_collection = RevokedToken
        checkout_product_collection = CheckoutProduct
        subscription_collection = Subscription

        # Return the client and collection references
        return client, user_collection, service_collection, revoked_token_collection, checkout_product_collection, subscription_collection

    except Exception as e:
        print(e)
        return None, None, None, None, None, None


def AddUser(name: str, surname: str, email: str, password: str) -> bool:
    try:
        users_collection = User._get_collection()
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
    
def GetUser(email: str) -> dict:
    """Get a user from the database.

    Args:
        email (str): The user's email.

    Returns:
        dict: The user's data.
        None: If the user does not exist.
    """
    try:
        users_collection = User._get_collection()
        user = users_collection.find_one({'email': email})
        return user if user else None
    except Exception as e:
        print(e)
        return None
    
def GetUserByStripeCustomerId(stripeCustomerId:str) -> dict:
    """Get a user from the database.

    Args:
        stripeCustomerId (str): The user's stripe customer id.

    Returns:
        dict: The user's data.
        None: If the user does not exist.
    """
    try:
        users_collection = User._get_collection()
        user = users_collection.find_one({'stripeCustomerId': stripeCustomerId})
        return user if user else None
    except Exception as e:
        print(e)
        return None
    
def AddTokens(email:str, tokens:int) -> bool:
    """Add tokens to a user's account.

    Args:
        email (str): The user's email.
        tokens (int): The number of tokens to add.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        users_collection = User._get_collection()
        user = users_collection.find_one({'email': email})
        if user:
            users_collection.update_one({'email': email}, {'$inc': {'tokens': tokens}})
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def GetCheckoutProduct(id:str) -> dict:
    """Get a checkout product from the database.

    Args:
        id (str): The checkout product's id.

    Returns:
        dict: The checkout product's data.
        None: If the checkout product does not exist.
    """
    try:
        checkout_products_collection = CheckoutProduct._get_collection()
        checkout_product = checkout_products_collection.find_one({'id': id})
        return checkout_product if checkout_product else None
    except Exception as e:
        print(e)
        return None

def GetSubcription(id:str) -> dict:
    """Get a subscription from the database.

    Args:
        id (str): The subscription's id.

    Returns:
        dict: The subscription's data.
        None: If the subscription does not exist.
    """
    try:
        subscriptions_collection = Subscription._get_collection()
        subscription = subscriptions_collection.find_one({'id': id})
        return subscription if subscription else None
    except Exception as e:
        print(e)
        return None
    

def SetUserSubscribed(email:str, subscribed:bool) -> bool:
    """Set a user's subscription status.

    Args:
        email (str): The user's email.
        subscribed (bool): The subscription status.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        users_collection = User._get_collection()
        user = users_collection.find_one({'email': email})
        if user:
            users_collection.update_one({'email': email}, {'$set': {'subscribed': subscribed}})
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    

def SetUserTokens(email:str, tokens:int) -> bool:
    """Set a user's tokens.

    Args:
        email (str): The user's email.
        tokens (int): The user's tokens.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        users_collection = User._get_collection()
        user = users_collection.find_one({'email': email})
        if user:
            users_collection.update_one({'email': email}, {'$set': {'tokens': tokens}})
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def SetUserStripeCustomerId(email:str, stripeCustomerId:str) -> bool:
    """Set a user's stripe customer id.

    Args:
        email (str): The user's email.
        stripeCustomerId (str): The user's stripe customer id.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        users_collection = User._get_collection()
        user = users_collection.find_one({'email': email})
        if user:
            users_collection.update_one({'email': email}, {'$set': {'stripeCustomerId': stripeCustomerId}})
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def AddRevokedToken(token:str) -> bool:
    """Add a revoked token to the database.

    Args:
        token (str): The revoked token.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        revoked_tokens_collection = RevokedToken._get_collection()
        if revoked_tokens_collection.find_one({'token': token}) is None:
            revoked_tokens_collection.insert_one({'token': token})
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def IsTokenRevoked(token:str) -> bool:
    """Check if a token has been revoked.

    Args:
        token (str): The token to check.

    Returns:
        bool: True if the token has been revoked, False otherwise.
    """
    try:
        revoked_tokens_collection = RevokedToken._get_collection()
        revoked_token = revoked_tokens_collection.find_one({'token': token})
        if revoked_token:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return True    

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
    
def GetService(name: str) -> dict:
    """Get a service from the database.

    Args:
        name (str): The service's name.

    Returns:
        dict: The service's data.
        None: If the service does not exist.
    """
    try:
        Services_collection = Service._get_collection()
        service = Services_collection.find_one({'name': name})
        return service if service else None
    except Exception as e:
        print(e)
        return None