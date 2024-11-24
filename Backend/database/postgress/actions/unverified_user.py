## TO BE REFACTORED

# from database.postgress.models.user import User
# from database.postgress.models.unverified_user import UnverifiedUser
# from modules.session_management.password import verify_password, hash_password
# from database.postgress.actions.role import get_role_by_name

# from sqlmodel import Session
# from sqlalchemy.exc import IntegrityError, OperationalError
# from datetime import datetime , timedelta

# # Create functions
# def CreateUnverifiedUser(session: Session, username: str, password: str, verification_token: str,  first_name: str | None = None, last_name: str | None = None,pending_role:str = "Young Person", phone_number: str | None = None, address: str | None = None, token_expires: datetime | None = None, hashed=False, commit = True, fresh=False) -> UnverifiedUser:
#     """ Create a POTENSIAL user in the database via standard registration (Password)

#     Args:
#         session (Session): The database session
#         username (str): The user's email
#         password (str): The user's password
#         verification_token (str): The user's verification token
#         first_name (str, optional): The user's first name. Defaults to None.
#         last_name (str, optional): The user's last name. Defaults to None.
#         pending_role (str, optional): The user's pending role. Defaults to "Young Person".
#         phone_number (str, optional): The user's phone number. Defaults to None.
#         address (str, optional): The user's address. Defaults to None.
#         token_expires (datetime, optional): The time the token expires. Defaults to None.
#         hashed (bool, optional): Whether the password given is hashed. Defaults to False.
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.
#         fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False
#     """
#     if token_expires is None:
#         # exprires in 1 day by default
#         token_expires = datetime.utcnow() + timedelta(days=1)
#     try:
#         if not hashed:
#             password = hash_password(password)
#         role_id = get_role_by_name(session, pending_role).role_id
#         if not role_id:
#             print("Role not found")
#             return None
#         user = UnverifiedUser(email=username, password_hash=password,pending_role=role_id, verification_token=verification_token, token_expires=token_expires, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
#         session.add(user)
#         if commit:
#             session.commit()
#         if fresh:
#             session.refresh(user)  # Ensure the user object is not expired
#         return user
#     except IntegrityError:
#         session.rollback()
#         print("A user with this email already exists.")
#         return None
#     except OperationalError:
#         session.rollback()
#         print("There was an issue with the database operation.")
#         return None
#     except TypeError as e:
#         session.rollback()
#         print(f"Type error: {e}")
#         return None

# # Get functions

# def get_unverified_user_by_email(session: Session, email: str):
#     """ Get an unverified user from the database by email """
#     return session.query(UnverifiedUser).filter(UnverifiedUser.email == email).first()

# def get_unverified_user_by_id(session: Session, user_id: int):
#     """ Get an unverified user from the database by ID """
#     return session.query(UnverifiedUser).filter(UnverifiedUser.unverified_user_id == user_id).first()

# def get_unverified_user_by_verification_token(session: Session, verification_token: str):
#     """ Get a user from the database by verification token """
#     return session.query(UnverifiedUser).filter(UnverifiedUser.verification_token == verification_token).first()

# # Update functions

# def verify_user(session: Session, user: UnverifiedUser, commit = True, fresh=False) -> User:
#     """ Verify a user in the database

#     Args:
#         session (Session): The database session
#         user (UnverifiedUser): The user object
#         commit (bool, optional): Whether to commit the transaction. Defaults to True.
#         fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False
#     """
#     try:
#         user = User(email=user.email, password_hash=user.password_hash,role_id=user.pending_role ,first_name=user.first_name, last_name=user.last_name, phone_number=user.phone_number, address=user.address)
#         session.add(user)
#         session.delete(user)
#         if commit:
#             session.commit()
#         if fresh:
#             session.refresh(user)
#         return user
#     except IntegrityError:
#         session.rollback()
#         print("A user with this email already exists.")
#         return None
#     except OperationalError:
#         session.rollback()
#         print("There was an issue with the database operation.")
#         return None
#     except TypeError as e:
#         session.rollback()
#         print(f"Type error: {e}")
#         return None

# # Delete functions

# def delete_unverified_user(session: Session, user: UnverifiedUser, commit=True) -> bool:
#     """ Delete a user from the database.
#     Args:
#         session (Session): The database session
#         user (UnverifiedUser): The user object
#         commit (bool, optional): Whether to commit the transaction. Defaults"""
#     try:
#         session.delete(user)
#         if commit:
#             session.commit()
#         return True
#     except:
#         return False

# def delete_unverified_users(session: Session, users: list[UnverifiedUser], commit=True) -> bool:
#     """ Delete a list of users from the database """
#     try:
#         for user in users:
#             if not delete_unverified_user(session, user, commit=False):
#                 print(f"Failed to delete user {user.email}")
#                 session.rollback()
#                 return False
#         if commit:
#             session.commit()
#         return True
#     except:
#         session.rollback()
#         return False
    
# def delete_expired_unverified_users(session: Session, commit=True) -> bool:
#     """ Delete all expired unverified users from the database 
    
#     Args:
#         session (Session): The database session
#         commit (bool, optional): Whether to commit the transaction. Defaults to True."""
#     try:
#         session.query(UnverifiedUser).filter(UnverifiedUser.token_expires < datetime.utcnow()).delete()
#         if commit:
#             session.commit()
#         return True
#     except:
#         return False