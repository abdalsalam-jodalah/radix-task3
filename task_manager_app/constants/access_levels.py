from enum import Enum

class AccessLevel(Enum):
    ALL = "all"
    OWN_BELOW = "own+below"
    OWN = "own"
    STATUS = "status"
