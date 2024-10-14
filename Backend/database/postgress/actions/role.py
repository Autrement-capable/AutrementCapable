from database.postgress.models.role import Role

from sqlmodel import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime , timedelta

# Create functions

def create_role(Session:Session, name:str, desc:str, commit=True, refresh=False ):
    """ Create a role in the database

    Args:
        Session (Session): The database session
        name (str): The role's name
        desc (str): The role's description
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        refresh (bool, optional): Whether to refresh the role object from DB(usefull if you want to manipulate it). Defaults to False.
    """
    role = Role(role_name=name, description=desc)
    Session.add(role)
    if commit:
        Session.commit()
    if refresh:
        Session.refresh(role)
    return role

# Get functions

def get_role_by_name(Session:Session, name:str):
    """ Get a role from the database by name """
    return Session.query(Role).filter(Role.role_name == name).first()

def get_role_by_id(Session:Session, role_id:int):
    """ Get a role from the database by ID """
    return Session.query(Role).filter(Role.role_id == role_id).first()

def get_all_roles(Session:Session):
    """ Get all roles from the database """
    return Session.query(Role).all()

# Update functions

def update_role(Session:Session, role:Role, commit=True, refresh=False):
    """ Update a role in the database

    Args:
        Session (Session): The database session
        role (Role): The role object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
        refresh (bool, optional): Whether to refresh the role object from DB(usefull if you want to manipulate it). Defaults to False.
    """
    Session.add(role)
    if commit:
        Session.commit()
    if refresh:
        Session.refresh(role)
    return role

# Delete functions

def delete_role(Session:Session, role:Role, commit=True) -> bool:
    """ Delete a role from the database

    Args:
        Session (Session): The database session
        role (Role): The role object
        commit (bool, optional): Whether to commit the transaction. Defaults to True.
    """
    try:
        Session.delete(role)
        if commit:
            Session.commit()
        return True
    except:
        return False