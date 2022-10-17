import tools.arguments_parser as arguments_parser
from tools.wave_file import WaveFile
import core.common as common
import json

"""
lsb_file follows same logic as lsb_basic but bits to hide are taken from file to hide and not message.
We hide data in sequence and generate a key(base64 of object containing original file name and amount of bits to extract
from file).

Extract by providing the wav file with the hidden data and the key
"""

def hide(filename):
    filename_to_hide = arguments_parser.parse_filename_to_hide()

    if not filename_to_hide.isascii():
        print('The name of the file to hide should contain only ascii characters')
        return

    file_to_hide = open(filename_to_hide, 'rb')
    bin_data = file_to_hide.read()
    
    message_bits_str = ''
    for data_byte in bin_data:
        message_bits_str += bin(data_byte).lstrip('0b').rjust(8,'0')

    message_bits = list(map(int, message_bits_str))

    file = WaveFile(filename)
    alter_every = int(file.BitsPerSample / 8)

    if int(len(file.data) / alter_every) < len(message_bits):
        print('File too small to store this file!')
        return

    data_index = 0
    for index in range(len(message_bits)):
        file.data[data_index] = (file.data[data_index] & 254) | message_bits[index]
        data_index += alter_every

    output_filename = common.get_output_filename('lsb_file')
    file.save_file(output_filename)

    file_to_hide.close()
    
    print('Successfully created new file with hidden file in it')

    personal_object = {
        'bits_count': len(message_bits),
        'filename': filename_to_hide
    }
    personal_key = common.to_base64(json.dumps(personal_object))

    key_filename = common.get_personal_key_filename('lsb_file')
    with open(key_filename, 'w') as file:
        file.write(personal_key)

    print(f'Your key for extracting data in {key_filename} file')
    

def extract(filename):
    personal_key_b64 = arguments_parser.parse_personal_key()
    personal_key = common.from_base64(personal_key_b64)
    personal_object = json.loads(personal_key)

    file = WaveFile(filename)
    extract_every = int(file.BitsPerSample / 8)

    bits = ''

    for index in range(0, len(file.data), extract_every):
        bits += str(file.data[index] & 1)
        if len(bits) == personal_object['bits_count']:
            break

    hidden_filename = personal_object['filename']

    binary_data = int(bits, 2).to_bytes(length=int(len(bits)/8), byteorder='big')
    with open(hidden_filename, 'wb') as file:
        file.write(binary_data)

    print(f'Successfully extracted the file - {hidden_filename}')