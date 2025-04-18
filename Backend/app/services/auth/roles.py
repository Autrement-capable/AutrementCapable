import copy

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...db.postgress.models import Role

roles = {
    "Super Admin": {
        "description": "Full system access for technical maintenance.",
        "role_id": 1
    },
    "Admin": {
        "description": "Manage users and platform configurations.",
        "role_id": 2
    },
    "Moderator": {
        "description": "Oversee community interactions and enforce guidelines.",
        "role_id": 3
    },
    "Accompagnateur": {
        "description": "Provide support and guidance to young persons.",
        "role_id": 4
    },
    "Expert": {
        "description": "Offer specialized insights and training content.",
        "role_id": 5
    },
    "Professional": {
        "description": "Provide job opportunities and professional advice.",
        "role_id": 6
    },
    "Parent": {
        "description": "Support and monitor their child's progress.",
        "role_id": 7
    },
    "Young Person": {
        "description": "Primary users seeking support and integration.",
        "role_id": 8
    },
    "Guest": { # not using this role for now
        "description": "Limited access to public features and information.",
        "role_id": 9
    }
}

async def init_roles(session: AsyncSession):
    """ Initialize the roles in the database. Skip roles that already exist."""
    try:
        statement = select(Role.role_name)
        result = await session.execute(statement)
        existing_role_names = {row[0] for row in result.all()}
        
        # Create a deep copy of the roles dictionary
        roles_to_add = copy.deepcopy(roles)
        
        # Remove roles that already exist
        for role_name in existing_role_names:
            roles_to_add.pop(role_name, None)
        
        # If all roles exist, return True
        if not roles_to_add:
            return True
        
        # Add the remaining roles to the database
        new_roles = [Role(role_name=role_name, description=role_data["description"]) for role_name, role_data in roles_to_add.items()]
        session.add_all(new_roles)
        await session.commit()
        return True
    except Exception as e:
        print(e)
        await session.rollback()
        return False