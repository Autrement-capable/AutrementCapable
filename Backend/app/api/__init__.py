from os import getenv
from .auth import *
from .data import *

if getenv("MODE") == "DEV":
    from .dev import *