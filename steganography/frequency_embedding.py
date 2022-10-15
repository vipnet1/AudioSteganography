from tools.wave_file import WaveFile
import tools.arguments_parser as arguments_parser
import core.constants as constants
from enums.positivity import Positivity
import core.common as common

def hide(filename):
    message = arguments_parser.parse_message()

    if '#' in message:
        print('# is special character, do not use it in message!')
        return

    message += '#'
    message_bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

    file = WaveFile(filename)

    change_sign_samples = int((file.SampleRate / constants.FREQUENCY_TO_EMBED) / 2)
    if change_sign_samples < 1:
        print(f'Sample rate is {file.SampleRate}. Cant embed hidden waves for desired frequency')
        return

    bytes_per_sample = int(file.BitsPerSample / 8)

    channels_positivity = [] # 0 means any, 1 positive, -1 negative
    for _ in range(file.NumChannels):
        channels_positivity.append(Positivity.NEUTRAL)

    new_data = []

    message_index = 0
    data_index = 0
    finished_hidding = False
    while data_index < len(file.data):
        can_embed = True

        for channel in range(file.NumChannels):
            # get over smaller bytes
            for _ in range(bytes_per_sample - 1):
                new_data.append(file.data[data_index])
                data_index += 1

            # we are on significant byte of sample
            positivity = Positivity.POSITIVE if file.data[data_index] < 128 else Positivity.NEGATIVE
            if channels_positivity[channel].value == positivity:
                can_embed = False

            new_data.append(file.data[data_index])
            data_index += 1

            channels_positivity[channel] = positivity

        if finished_hidding or not can_embed:
            continue

        for samples_to_swap in [change_sign_samples - 1, change_sign_samples, 1]:
            for _ in range(samples_to_swap):
                for channel_num in range(file.NumChannels):
                    for _ in range(bytes_per_sample - 1):
                        if finished_hidding:
                            byte_data = int('0'*8, 2)
                            new_data.append(byte_data)
                            continue

                        byte_data = int("".join(str(bit) for bit in message_bits[message_index : message_index + 8]).ljust(8,'0'), 2)
                        new_data.append(byte_data)
                        message_index += 8

                        if message_index >= len(message_bits): finished_hidding = True

                    if finished_hidding:
                        byte_data = int('0' if channels_positivity[channel_num] == Positivity.POSITIVE else '1' + '0'*7, 2)
                        new_data.append(byte_data)
                        continue

                    byte_data = int('0' if channels_positivity[channel_num] == Positivity.POSITIVE else '1' + "".join(str(bit) for bit in message_bits[message_index : message_index + 7]).ljust(7,'0'), 2)
                    new_data.append(byte_data)
                    message_index += 7
            
            # switch positivity
            channels_positivity[channel_num] =  Positivity.NEGATIVE if channels_positivity[channel_num] == Positivity.POSITIVE else Positivity.NEGATIVE

            

            

        

    file.replace_data_block(new_data)

    output_filename = common.get_output_filename('lsb_basic')
    file.save_file(output_filename)

    print('yo')
    

def extract(filename):
    pass