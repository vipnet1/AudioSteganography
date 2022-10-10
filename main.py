import sys
import json
import tools.aes_cipher as aes_cipher

from enums.command import Command
from enums.data_type import DataType

# public_key = aes_cipher.generate_key()
public_key = b'\x9b\xda\xeaH\xec\x98\xda\x9f\xf8Lw\x1d&\xc2X\x8a'


def hide(data_type):
    personal_object  = {'hello': 'there'}
    personal_object_bytes = json.dumps(personal_object).encode('ascii')

    personal_key = aes_cipher.encrypt(public_key, personal_object_bytes).decode('utf-8')
    return personal_key

def extract(personal_key_str):
    personal_key_bytes = personal_key_str.encode('ascii')
    personal_object = json.loads(aes_cipher.decrypt(public_key, personal_key_bytes))
    return personal_object


def handle_command_hide():
    if len(sys.argv) < 4:
        print('You must provide more arguments!')
        return

    data_type = sys.argv[2]
    if not DataType.has_value(data_type):
        print('Wrong data type - Terminating...')
        return

    personal_key = hide(data_type)

    print(f'Successfully hidden data.\nYour personal key for recovering it: {personal_key}')

def handle_command_extract():
    if len(sys.argv) < 4:
        print('You must provide more arguments!')
        return

    personal_key_str = sys.argv[3]
    message = extract(personal_key_str)
    print(f'Successfully extracted data - {message}')


#
# PARAMS CASE HIDING
# python main.py hide text THE_TEXT_TO_HIDE
# or
# python main.py hide file FILEPATH_TO_HIDE
#
# PARAMS CASE EXTRACTING
# python main.py extract filename PERSONAL_KEY_STRING
#
def main():
    if len(sys.argv) < 2:
        print('You must provide command!')
        return

    command = sys.argv[1]
    if not Command.has_value(command):
        print('Wrong command type - Terminating...')
        return

    functions = {
        Command.HIDE: handle_command_hide,
        Command.EXTRACT: handle_command_extract
    }

    functions[Command[command.upper()]]()