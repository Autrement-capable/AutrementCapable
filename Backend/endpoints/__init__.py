# Import new endpoints
from os import getenv

from .data import *
from .auth import *

if getenv("MODE") == "DEV":
    from .dev import *