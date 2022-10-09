from enum import Enum

class Command(Enum):
    HIDE = 'hide'
    EXTRACT = 'extract'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_