# Setup for the postgress database. import all the models here. after the postgress object is created
#  the models will be added to the database.
from database.postgress.config import postgress
from database.postgress.models.example import Example
from database.postgress.models.oauth_provider import OAuthProvider
from database.postgress.models.passkey import Passkey
from database.postgress.models.user import User
from database.postgress.models.password_reset import PasswordReset
from database.postgress.models.young_person import YoungPerson
from database.postgress.models.unverified_user import UnverifiedUser
from database.postgress.models.revokedTokens import RevokedToken

_all_ = ["postgress"]