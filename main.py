import tools.arguments_parser as arguments_parser

from enums.command import Command
from enums.algorithm import Algorithm

import steganography.lsb_basic as lsb_basic
import steganography.lsb_key_based as lsb_key_based
import steganography.lsb_file as lsb_file


def handle_command_hide():
    algorithm = arguments_parser.parse_algorithm()
    filename = arguments_parser.parse_filename()

    functions = {
        Algorithm.LSB_BASIC: lsb_basic.hide,
        Algorithm.LSB_KEY_BASED: lsb_key_based.hide,
        Algorithm.LSB_FILE: lsb_file.hide
    }

    functions[Algorithm[algorithm.upper()]](filename)

def handle_command_extract():
    algorithm = arguments_parser.parse_algorithm()
    filename = arguments_parser.parse_filename()

    functions = {
        Algorithm.LSB_BASIC: lsb_basic.extract,
        Algorithm.LSB_KEY_BASED: lsb_key_based.extract,
        Algorithm.LSB_FILE: lsb_file.extract
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