from sqlmodel import Relationship
from typing import List, Optional

# Import all models
from database.postgress.config import postgress
# from database.postgress.models.role import Role
# from database.postgress.models.password_reset import PasswordReset
# from database.postgress.models.user import User
# from database.postgress.models.unverified_user import UnverifiedUser
# from database.postgress.models.revokedTokens import RevokedToken

import database.postgress.models.test_model

_all_ = ["postgress"]