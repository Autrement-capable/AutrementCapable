
tmp_db = {} # !!!TEMPORARY
revoked_tokens = set() # !!!TEMPORARY

def GetUser(username):
    """Get a user from the database by the username. Will return None if the user does not exist."""
    return tmp_db.get(username, None)

def AddUser(name, username, email, password):
    """Add a user to the database. Will return the user if it was added successfully."""
    if not GetUser(username):
        tmp_db[username] = {
            "name": name,
            "username": username,
            "email": email,
            "password": password
        }
        return tmp_db[username]
    return False

def DeleteUser(username):
    """Delete a user from the database. Will return False if the user does not exist.
    Will return True if the user was deleted successfully."""
    if GetUser(username):
        del tmp_db[username]
        return True
    return False

def GetRevokedTokens():
    """ TEMPORARY METHOD
    Get the set of revoked tokens.
    Returns:
        set: The set of revoked tokens.
    """
    return revoked_tokens

def AddRevokedToken(jwt):
    """ TEMPORARY METHOD
    Add a revoked token to the set of revoked tokens."""
    revoked_tokens.add(jwt)