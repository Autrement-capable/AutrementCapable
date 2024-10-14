from database.postgress.models.user import User
from database.postgress.actions.role import get_role_by_name
from modules.session_management.password import verify_password, hash_password

from sqlmodel import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime , timedelta


# Create functions

def create_user(session: Session, username: str, email:str, password: str, first_name: str | None = None, last_name: str | None = None, role_name:str = "Young Person", phone_number: str | None = None, address: str | None = None, hashed=False, commit = True, fresh=False) -> User:
    """ Create a user in the database via standard registration (Password)

    Args:
        session (Session): The database session
        email (str): The user's email
        username (str): The user's username
        password (str): The user's password
        first_name (str, optional): The user's first name. Defaults to None.
        last_name (str, optional): The user's last name. Defaults to None.
        role_name (str, optional): The user's role. Defaults to "Young Person".
        phone_number (str, optional): The user's phone number. Defaults to None.
        address (str, optional): The user's address. Defaults to None.
        hashed (bool, optional): Whether the password given is hashed. Defaults to False.
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False."""
    try:
        if not hashed:
            password = hash_password(password)
        role_id = get_role_by_name(session, role_name).role_id
        if not role_id:
            print("Role not found")
            return None
        user = User(username=username, email=email, password_hash=password, role_id=role_id, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        session.add(user)
        if commit:
            session.commit()
        if fresh:
            session.refresh(user)  # Ensure the user object is not expired
        return user
    except IntegrityError:
        session.rollback()
        print("A user with this email already exists.")
        return None
    except OperationalError:
        session.rollback()
        print("There was an issue with the database operation.")
        return None
    except TypeError as e:
        session.rollback()
        print(f"Type error: {e}")
        return None


def create_oauth_user():
    """ Create a user in the database via OAuth """
    pass


# i dont know if we can even create a user with passkey alone
def create_passkey_user():
    """ Create a user in the database via Passkey """
    pass

# Get functions

def get_user_by_email(session: Session, email: str) -> User:
    """ Get a user from the database by email """
    return session.query(User).filter(User.email == email).first()

def get_user_by_username(session: Session, username: str) -> User:
    """ Get a user from the database by username """
    return session.query(User).filter(User.username == username).first()

def get_all_usernames(session: Session) -> list[str]:
    """ Get all usernames from the database """
    return [user.username for user in session.query(User).all()]

def is_username_taken(session: Session, username: str) -> bool:
    """ Check if a username is already taken """
    return bool(session.query(User).filter(User.username == username).first())

def get_user_by_id(session: Session, user_id: int) -> User:
    """ Get a user from the database by ID """
    return session.query(User).filter(User.user_id == user_id).first()

def login_user(session: Session, password: str,  username_email: str, hashed=False) -> User | None:
    """ Log a user in via standard registration (Password) using their username or email

    Args:
        session (Session): The database session
        password (str): The user's password
        username_email (str): The user's username or email
        hashed (bool, optional): Whether the password is hashed. Defaults to False.

        Returns:
            User | None: The user object if the login was successful, None otherwise"""

    user = get_user_by_username(session, username_email) # check if the username exists
    if not user:
        user = get_user_by_email(session, username_email) # check if the email exists

    if not user:
        return None

    if (not hashed and not verify_password(password, user.password_hash)) or \
   (hashed and password != user.password_hash):
        return None

    return user


## Update functions

def Update_user(session: Session, user: User, commit=True, fresh=False) -> User|None:
    """ Update a user in the database

    Args:
        session (Session): The database session
        user (User): The user object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        fresh (bool, optional): Whether to refresh the user object from DB(usefull if you want to manipulate it). Defaults to False."""
    try:
        session.add(user)
        if commit:
            session.commit()
        if fresh:
            session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        print("A user with this email already exists.")
        return None
    except OperationalError:
        session.rollback()
        print("There was an issue with the database operation.")
        return None
    except TypeError as e:
        session.rollback()
        print(f"Type error: {e}")
        return None

# Delete functions

def delete_user(session: Session, user: User, commit=True) -> bool:
    """ Delete a user from the database

    Args:
        session (Session): The database session
        user (User): The user object
        commit (bool, optional): Whether to commit the transaction. Defaults to True."""
    try:
        session.delete(user)
        if commit:
            session.commit()
        return True
    except:
        return False
