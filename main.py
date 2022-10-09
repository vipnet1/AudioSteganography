import wave
import sys
import aes_cipher
import json

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

main()








# def lsb_hide(src_filename, dest_filename, bits):

#     if not secret.isascii():
#         print('Currently we support only hiding ascii characters... terminating process')
#         return

#     # read wave audio file
#     song = wave.open(src_filename, mode='rb')

#     # Read frames and convert to byte array
#     frame_bytes = bytearray(list(song.readframes(song.getnframes())))

#     string = secret

#     # Append dummy data to fill out rest of the bytes.
#     string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'

#     # Convert text to bit array
#     bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

#     # Replace LSB of each byte of the audio data by one bit from the text bit array
#     for i, bit in enumerate(bits):
#         frame_bytes[i] = (frame_bytes[i] & 254) | bit

#     # Get the modified bytes
#     frame_modified = bytes(frame_bytes)

#     # Write bytes to a new wave audio file
#     with wave.open(dest_filename, 'wb') as fd:
#         fd.setparams(song.getparams())
#         fd.writeframes(frame_modified)

#     song.close()

#     print(f'Successfully hide secret inside file {dest_filename}')

# def lsb_extract(filename):
#     song = wave.open(filename, mode='rb')

#     # Convert audio to byte array
#     frame_bytes = bytearray(list(song.readframes(song.getnframes())))

#     # Extract the LSB of each byte
#     extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

#     # Convert byte array back to string
#     string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    
#     # Cut off at the filler characters
#     decoded = string.split("###")[0]

#     # Print the extracted text
#     print("Sucessfully decoded: "+decoded)

#     song.close()