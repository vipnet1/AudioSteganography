from enum import Enum

class Algorithm(Enum):
    LSB_BASIC = 'lsb_basic'
    LSB_KEY_BASED = 'lsb_key_based'
    FREQUENCY_EMBEDDING = 'frequency_embedding'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_