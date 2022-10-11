import tools.arguments_parser as arguments_parser
from tools.wave_file import WaveFile
import core.common as common
import core.constants as constants

def hide(filename):
    message = arguments_parser.parse_message()

    if '#' in message:
        print('# is special character, do not use it in message!')
        return

    message += '#'

    file = WaveFile(filename)

    # samples count for embedded wave to be on correct frequency
    samples_count = int((float(file.SampleRate) / constants.FREQUENCY_TO_HIDE_ON) / 2)
    if samples_count == 0:
        print('Too small sample rate - cant embed waves with correct frequency')
        return

    message_bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

    last_altered_index = 0
    is_last_positive = True

    bytes_per_sample = int(file.BitsPerSample / 8)

    msg_bit_index = 0

    new_data = []

    index = 0
    while index < len(file.data):
        is_most_significant_byte = index % bytes_per_sample == (bytes_per_sample - 1)
        is_positive = file.data[index] < 128

        if msg_bit_index >= len(message_bits) or \
             not is_most_significant_byte or is_positive == is_last_positive or \
                last_altered_index + constants.FREQUENCY_EMBED_EVERY_SAMPLES > index:
            new_data.append(file.data[index])

            is_last_positive = is_positive
            index += 1
            continue

        now_positive = not is_positive
        for _ in range(samples_count):
            num = 0 if now_positive else 128

            binary_str = ''.join(str(bit) for bit in message_bits[msg_bit_index:msg_bit_index + 7])
            binary_str = binary_str.rjust(7,'0')

            num += int(binary_str, 2) >> 1

            new_data.append(num)
            now_positive = not now_positive

            msg_bit_index += 7

        last_altered_index = index

        new_data.append(file.data[index])
        is_last_positive = is_positive
        index += 1

    if msg_bit_index < len(message_bits):
        print('Too small file to hide message')
        return

    output_filename = common.get_output_filename()
    file.save_file(output_filename)

    print('Successfully created new file with hidden message')

def extract(filename):
    pass