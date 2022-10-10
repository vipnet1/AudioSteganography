import tools.arguments_parser as arguments_parser
from tools.wave_file import WaveFile
import core.common as common

# lsb_basic alters lsb of least significant bytes sequently from beginning of data section. '#' character means
# we extracted whole message.
# Pros - no key needed because whole message located at the beginning.
# Cons -  may be easier to notice change in audio all changes made in beginning of file. Also anyone holding file can recover message as there's no key


# data stored in little endian. BitsPerSample indicates how many bits for each audio sample. So - if we
# want to store via lsb we need to be sure that we do it also in least significant byte.
# for example if BitsPerSample=16 audio data stored in 2 bytes. It's little endian - so we want to alter
# the lsb of byte 0,2,4... because they are least significant. This will make change unnoticeable for humans.
# in message each character ascii so 1 byte - 8 bits. Every 8 bits we can build character. Lets suppose
# if character is '#' means whole message extracted
def hide(filename):
    message = arguments_parser.parse_message()

    if '#' in message:
        print('# is special character, do not use it in message!')
        return

    message += '#'

    file = WaveFile(filename)
    alter_every = int(file.BitsPerSample / 8)

    if int(len(file.data) / alter_every) < len(message) * 8:
        print('File too small to store message!')
        return

    message_bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

    data_index = 0
    for index in range(len(message_bits)):
        file.data[data_index] = (file.data[data_index] & 254) | message_bits[index]
        data_index += alter_every

    output_filename = common.get_output_filename()
    file.save_file(output_filename)

    print('Successfully created new file with hidden message')
    

def extract(filename):
    file = WaveFile(filename)
    extract_every = int(file.BitsPerSample / 8)

    char_bits = ''
    message = ''

    for index in range(0, len(file.data), extract_every):
        char_bits += str(file.data[index] & 1)
        if len(char_bits) == 8:
            decimal_num = int(char_bits, 2)
            character = chr(decimal_num)

            if character == '#':
                break

            message += character
            char_bits = ''

    print(f'Successfully extracted the message - {message}')