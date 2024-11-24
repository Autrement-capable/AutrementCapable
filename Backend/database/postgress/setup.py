# Setup for the postgress database. import all the models here. after the postgress object is created
# put the relationships here cause circular imports are a pain
from sqlmodel import Relationship
from typing import List, Optional

# Import all models
from database.postgress.config import postgress
from database.postgress.models.role import Role
from database.postgress.models.oauth_provider import OAuthProvider
from database.postgress.models.passkey import Passkey
from database.postgress.models.user import User
from database.postgress.models.password_reset import PasswordReset
from database.postgress.models.young_person import YoungPerson
from database.postgress.models.unverified_user import UnverifiedUser
from database.postgress.models.revokedTokens import RevokedToken

# Setup relationships after models are defined

# Role relationships
Role.users = Relationship(back_populates="role")

# User relationships
User.role = Relationship(back_populates="users")
User.oauth_providers = Relationship(back_populates="user")
User.passkeys = Relationship(back_populates="user")
User.password_resets = Relationship(back_populates="user")
User.young_person = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

# Passkey relationships
Passkey.user = Relationship(back_populates="passkeys")

# PasswordReset relationships
PasswordReset.user = Relationship(back_populates="password_resets")

# YoungPerson relationships
YoungPerson.user = Relationship(back_populates="young_person")

# UnverifiedUser relationships
UnverifiedUser.role = Relationship(back_populates="unverified_users")

# Role relationships (for UnverifiedUser)
Role.unverified_users = Relationship(back_populates="role")

# OAuthProvider relationships
OAuthProvider.user = Relationship(back_populates="oauth_providers")

_all_ = ["postgress"]