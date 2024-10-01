# Setup for the postgress database. import all the models here. after the postgress object is created
#  the models will be added to the database.
from database.postgress.config import postgress
from database.postgress.models.example import Example

_all_ = ["postgress"]