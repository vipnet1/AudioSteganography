import tools.arguments_parser as arguments_parser

from enums.command import Command
from enums.algorithm import Algorithm

import steganography.lsb_basic as lsb_basic
import steganography.lsb_key_based as lsb_key_based
import steganography.frequency_embedding as frequency_embedding

# def hide(data_type):
#     personal_object  = {'hello': 'there'}
#     personal_object_bytes = json.dumps(personal_object).encode('ascii')

#     personal_key = aes_cipher.encrypt(public_key, personal_object_bytes).decode('utf-8')
#     return personal_key

# def extract(personal_key_str):
#     personal_key_bytes = personal_key_str.encode('ascii')
#     personal_object = json.loads(aes_cipher.decrypt(public_key, personal_key_bytes))
#     return personal_object


def handle_command_hide():
    algorithm = arguments_parser.parse_algorithm()
    filename = arguments_parser.parse_filename()

    functions = {
        Algorithm.LSB_BASIC: lsb_basic.hide,
        Algorithm.LSB_KEY_BASED: lsb_key_based.hide,
        Algorithm.FREQUENCY_EMBEDDING: frequency_embedding.hide
    }

    functions[Algorithm[algorithm.upper()]](filename)

def handle_command_extract():
    algorithm = arguments_parser.parse_algorithm()
    filename = arguments_parser.parse_filename()

    functions = {
        Algorithm.LSB_BASIC: lsb_basic.extract,
        Algorithm.LSB_KEY_BASED: lsb_key_based.extract,
        Algorithm.FREQUENCY_EMBEDDING: frequency_embedding.extract
    }

    functions[Algorithm[algorithm.upper()]](filename)


def main():
    command = arguments_parser.parse_command()

    functions = {
        Command.HIDE: handle_command_hide,
        Command.EXTRACT: handle_command_extract
    }

    functions[Command[command.upper()]]()

main()