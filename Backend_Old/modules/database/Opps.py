from modules.config.Config import Config
from pymongo import MongoClient
from modules.database.Schema import *

# db:MongoClient = Config().GetDB()

# db_client = MongoClient(Config().GetDB())
# db = db_client.your_database_name  # Replace 'your_database_name' with your actual database name

# # Create collections for CheckoutProducts and Subscriptions
# checkout_products_collection = db.CheckoutProducts
# subscriptions_collection = db.Subscriptions
# users_collection = db.Users
# revoked_tokens_collection = db.RevokedTokens

#example of new collections for contains different types of services to be used by the user via token/subscriptions

Services_collection = {
    "1" : {
        "name" : "Service 1",
        "priceOriginal" : 10,
        "pricePremium" : 5,
        "description" : "This is a service that can be used by the user via tokens or subscription"
    },
    '2' : {
        "name" : "Service 2",
        "priceOriginal" : 3,
        "pricePremium" : 0,
        "description" : "This is a service that can be used by the user via tokens or subscription number 2"
    }
}

revoked_tokens =[] # this is temporary until we have a database
Tmp_DB = {} # this is temporary until we have a database
Tmp_DB_Data = {}
# Tmp_DB_Data_ID = 0

# TODO add the shcema for this table in an acual db
Tmp_DB['CheckoutProducts'] = {}
Tmp_DB['CheckoutProducts'][1] = {'name': 'token', 'price_id': 'price_1OD9XpFhDQtkCHA9r3KbUQ99', 'description': 'token used to access premium features'}

# TODO add the shcema for this table in an acual db
Tmp_DB['Subcriptions'] = {}
Tmp_DB['Subcriptions'][1] = {'name': 'subcription', 'price_id': 'price_1ORZZSFhDQtkCHA9n0TW3vPJ', 'description': 'subcription granting unlimited access premium features'}

def AddUser(name:str, surname:str, email:str, password:str) -> bool:
    """Add a user to the database.

    Args:
        name (str): The user's name.
        surname (str): The user's surname.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # TODO tmp code replace with actual db
        if email not in Tmp_DB:
            Tmp_DB[email] = {
                'id': len(name + surname + email + password),
                'name': name,
                'surname': surname,
                'email': email,
                'password': password,
                'subscribed': False,
                'tokens': 3,
                'stripeCustomerId': None
            }
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def GetUser(email:str) -> dict:
    """Get a user from the database.

    Args:
        email (str): The user's email.

    Returns:
        dict: The user's data.
        None: If the user does not exist.
    """
    # TODO tmp code replace with actual db
    if email in Tmp_DB:
        return Tmp_DB[email]
    else:
        return None

def GetUserByStripeCustomerId(stripeCustomerId:str) -> dict:
    """Get a user from the database.

    Args:
        stripeCustomerId (str): The user's stripe customer id.

    Returns:
        dict: The user's data.
        None: If the user does not exist.
    """
    # TODO tmp code replace with actual db
    for user in Tmp_DB:
        try: # because the Tmp_DB has other data in it it may error then accing the stripeCustomerId
            if Tmp_DB[user]['stripeCustomerId'] == stripeCustomerId:
                return Tmp_DB[user]
        except:
            continue
    return None

def AddTokens(email:str, tokens:int) -> bool:
    """Add tokens to a user.

    Args:
        email (str): The user's email.
        tokens (int): The amount of tokens to add.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # TODO tmp code replace with actual db
        if email in Tmp_DB:
            Tmp_DB[email]['tokens'] += tokens
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
    # TODO tmp code replace with actual db
    if id in Tmp_DB['CheckoutProducts']:
        return Tmp_DB['CheckoutProducts'][id]
    else:
        return None

def GetSubcription(id:str) -> dict:
    """Get a subcription from the database.

    Args:
        id (str): The subcription's id.

    Returns:
        dict: The subcription's data.
        None: If the subcription does not exist.
    """
    # TODO tmp code replace with actual db
    if id in Tmp_DB['Subcriptions']:
        return Tmp_DB['Subcriptions'][id]
    else:
        return None

def SetUserSubscribed(email:str, subscribed:bool) -> bool:
    """Set a user's subscription status.

    Args:
        email (str): The user's email.
        subscribed (bool): The user's subscription status.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
       # TODO tmp code replace with actual db
        if email in Tmp_DB:
            Tmp_DB[email]['subscribed'] = subscribed
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
       # TODO tmp code replace with actual db
        if email in Tmp_DB:
            Tmp_DB[email]['tokens'] = tokens
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
       # TODO tmp code replace with actual db
        if email in Tmp_DB and Tmp_DB[email] != None:
            Tmp_DB[email]['stripeCustomerId'] = stripeCustomerId
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def AddDataCollectionItem(userId:int, type:str, totalClicks:int) -> bool:
    """Add a item to the database.

    Args:
        userId (int): The user's id.
        surname (str): The type.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        None
    """
    try:
        # db[user_activities_collection_name].insert_one(
        #     { 'id': db[user_activities_collection_name].count_documents({}) + 1,
        #      'userId': userId, 'data-type': type, 'total-clicks': totalClicks
        #     })
        # Tmp_DB_Data_ID += 1
        Tmp_DB_Data[f"{userId}-{type}"] = {'id': 1, 'userId': userId, 'data-type': type, 'total-clicks': totalClicks}
        return True
    except Exception as e:
        print(e)
        return False
    
def EditDataCollectionItem(id:int, userId: int, type: str, totalClicks:int) -> bool:
    """Add a item to the database.

    Args:
        userId (int): The user's id.
        surname (str): The type.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        None
    """
    try:
        # db[user_activities_collection_name].update_one(
        #     {'id': id},
        #     { 'id': id,
        #      'userId': userId, 'data-type': type, 'total-clicks': totalClicks
        #     })
        Tmp_DB_Data[f"{userId}-{type}"]["total-clicks"] = totalClicks
        return True
    except Exception as e:
        print(e)
        return False

def GetDataCollectionItem(userId: int, type: str) -> dict:
    """Get a data collection item from the database.

    Args:
        userId (int): The user's ID.
        type: data collection type.

    Returns:
        data collection item
    """
    try:
        # item = db[user_activities_collection_name].find_one({'userId': userId, 'data-type': type})
        item = Tmp_DB_Data[f"{userId}-{type}"]
        return item
    except Exception as e:
        print(e)
        return None
        
def getService(id:str) -> dict:
    """Get a service from the database.

    Args:
        id (str): The service's id.

    Returns:
        dict: The service's data.
        None: If the service does not exist.
    """
    # TODO tmp code replace with actual db
    if id in Services_collection:
        return Services_collection[id]
    else:
        return None

def AddRevokedToken(token:str) -> bool:
    """Add a revoked token to the database.

    Args:
        token (str): The token to add.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # TODO tmp code replace with actual db
        if token not in revoked_tokens:
            revoked_tokens.append(token)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def IsTokenRevoked(token:str) -> bool:
    """Check if a token is revoked.

    Args:
        token (str): The token to check.

    Returns:
        bool: True if the token is revoked, False otherwise.
    """
    try:
        # TODO tmp code replace with actual db
        if token in revoked_tokens:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False