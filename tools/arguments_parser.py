import sys
import os

from enums.command import Command
from enums.algorithm import Algorithm

ERROR_NO_ARGUMENT = 10
ERROR_WRONG_ARGUMENT = 11

def parse_command():
    if len(sys.argv) < 2:
        print('You must provide command!')
        sys.exit(ERROR_NO_ARGUMENT)

    command = sys.argv[1]
    if not Command.has_value(command):
        print('Wrong command type')
        sys.exit(ERROR_WRONG_ARGUMENT)

    return command

def parse_algorithm():
    if len(sys.argv) < 3:
        print('You must provide algorithm type!')
        sys.exit(ERROR_NO_ARGUMENT)

    algorithm = sys.argv[2]
    if not Algorithm.has_value(algorithm):
        print('Wrong algorithm type')
        sys.exit(ERROR_WRONG_ARGUMENT)

def parse_filename():
    if len(sys.argv) < 4:
        print('You must provide filename!')
        sys.exit(ERROR_NO_ARGUMENT)

    filename = sys.argv[3]
    if not os.path.exists(filename):
        print('File not found!')
        sys.exit(ERROR_WRONG_ARGUMENT)

    return filename

def parse_message():
    if len(sys.argv) < 5:
        print('You must provide message to hide!')
        sys.exit(ERROR_NO_ARGUMENT)

    message = sys.argv[4]
    return message

def parse_personal_key():
    if len(sys.argv) < 5:
        print('You must provide personal key!')
        sys.exit(ERROR_NO_ARGUMENT)

    personal_key = sys.argv[4]
    return personal_key