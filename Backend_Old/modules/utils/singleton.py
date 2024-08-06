
def singleton(cls):
    """A singleton decorator. Garantees that only one instance of the class is created."""
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
