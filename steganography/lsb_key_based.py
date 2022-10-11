import tools.arguments_parser as arguments_parser
from tools.wave_file import WaveFile
import core.common as common
import json
import random
import core.constants as constants

"""
lsb_key_based alters lsb of least significant bytes - like lsb_basic, but the locations are generated randomly and
not in sequence. Because of this randomized mechanism we can hide less data in the file than in lsb_basic.
after hidding message we get list of locations of each bit of message characters - I put it inside an object
serialize and base64 it and call it 'personal_key'. So to extract the data you need to provide this base64 key
so we know where and in what order to extract each bit of the message

Pros - file and key required to extract message - more secure.
       also all changes aren't sequently but in random positions - harder to notice changes.

Cons - can hide less data in same file(because of randomization).
       as the 'personal_key' is just base64 of locations it will grow larger as the message to hide grows larger.
"""

def hide(filename):
    message = arguments_parser.parse_message()

    file = WaveFile(filename)
    alter_every = int(file.BitsPerSample / 8)

    if int((len(file.data) / alter_every) * constants.ALTER_PERCENT_LSB_KEY_BASED) < len(message) * 8:
        print('File too small to store message! You may try different algorithm')
        return

    message_bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
    max_gen_limit = int(len(file.data) / alter_every)

    locations_set = set()
    locations_list = []

    for _ in range(len(message_bits)):
        while True:
            byte_location = random.randint(0, max_gen_limit) * alter_every
            if byte_location not in locations_set:
                break

        locations_set.add(byte_location)
        locations_list.append(byte_location)

    for index in range(len(message_bits)):
        location = locations_list[index]
        file.data[location] = (file.data[location] & 254) | message_bits[index]

    output_filename = common.get_output_filename()
    file.save_file(output_filename)

    print('Successfully created new file with hidden message')

    personal_object = {
        'locations': locations_list
    }

    personal_key = common.to_base64(json.dumps(personal_object))

    key_filename = common.get_personal_key_filename()
    with open(key_filename, 'w') as file:
        file.write(personal_key)

    print(f'Your key for extracting data in {key_filename} file')


def extract(filename):
    file = WaveFile(filename)

    personal_key_b64 = arguments_parser.parse_personal_key()
    personal_key = common.from_base64(personal_key_b64)
    personal_object = json.loads(personal_key)

    locations_list = personal_object['locations']

    char_bits = ''
    message = ''

    for location in locations_list:
        char_bits += str(file.data[location] & 1)

        if len(char_bits) == 8:
            decimal_num = int(char_bits, 2)
            character = chr(decimal_num)
            message += character
            char_bits = ''

    print(f'Successfully extracted the message - {message}')