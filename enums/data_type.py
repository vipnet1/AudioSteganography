from enum import Enum

class DataType(Enum):
    TEXT = 'text'
    # FILE = 'file'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_