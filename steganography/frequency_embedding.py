from tools.wave_file import WaveFile
import tools.arguments_parser as arguments_parser
import core.constants as constants
from enums.positivity import Positivity
import core.common as common

"""
frequency_embedding is an invented algorithm. We find the points were audio wave finished(swap from positive to negative or
vise versa) and embed wave in frequency that humans can't hear. Because of this the volume isn't important as we can't hear it
anyway so we use the volume bits to store the message bits. For example if BitsPerSample is 16 we use 15 of bits to store
message and most signiificant remains for frequency.

For example if SampleRate is 44100 so -> 44100 / 22050 = 2 -> what means if we finish audio wave in two samples human
can't hear it. And we use this technique to hide the message.

There may be case when we can't embed waves of desired frequency so in this case this method will not work.

This method increases file size.

The points where we embed the wave are where all channels close their old wave(positive becomes negative or vise versa for
all channels). At this point we embed the wave. We wait FE_EMBED_EVERY_SAMPLES samples before doing so again to not
make it noticeable.
"""

def hide(filename):
    message = arguments_parser.parse_message()

    if '#' in message:
        print('# is special character, do not use it in message!')
        return

    message += '#'
    message_bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

    file = WaveFile(filename)

    change_sign_samples = int((file.SampleRate / constants.FE_FREQUENCY_TO_EMBED) / 2)
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

    last_embedded_sample = 0
    current_sample = 0

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

        if finished_hidding or not can_embed or last_embedded_sample + constants.FE_EMBED_EVERY_SAMPLES > current_sample:
            current_sample += 1
            continue

        samples_to_swap_list = [change_sign_samples - 1, change_sign_samples, 1]

        for index in range(len(samples_to_swap_list)):
            samples_to_swap = samples_to_swap_list[index]

            for _ in range(samples_to_swap):
                for channel_num in range(file.NumChannels):
                    # if non significan bytes use all 8 bits to hide message
                    for _ in range(bytes_per_sample - 1):
                        if finished_hidding: # if finished hidding data store zeros for now, we will stop at the while loop
                            byte_data = int('0'*8, 2)
                            new_data.append(byte_data)
                            continue

                        byte_data = int("".join(str(bit) for bit in message_bits[message_index : message_index + 8]).ljust(8,'0'), 2)
                        new_data.append(byte_data)
                        message_index += 8

                        if message_index >= len(message_bits): finished_hidding = True

                    # even if finished hidding we want to maintain frequency and later continue with original sound
                    if finished_hidding:
                        byte_data = int('0' if channels_positivity[channel_num] == Positivity.POSITIVE else '1' + '0'*7, 2)
                        new_data.append(byte_data)
                        continue

                    # if significant byte use 7 bits to store message, and most significant for frequency
                    byte_data = int(('0' if channels_positivity[channel_num] == Positivity.POSITIVE else '1') + "".join(str(bit) for bit in message_bits[message_index : message_index + 7]).ljust(7,'0'), 2)
                    new_data.append(byte_data)
                    message_index += 7
            
            # dont switch positivity if returned to initial positivity
            if index == len(samples_to_swap_list) - 1:
                continue

            # switch channels positivity
            for chan_num in range(file.NumChannels):
                channels_positivity[chan_num] =  Positivity.NEGATIVE if channels_positivity[chan_num] == Positivity.POSITIVE else Positivity.POSITIVE
            
        last_embedded_sample = current_sample
        current_sample += 1

    if not finished_hidding:
        print('Cant hide whole message in the sound file')
        return
            

    file.replace_data_block(bytearray(new_data))

    output_filename = common.get_output_filename('frequency_embedding')
    file.save_file(output_filename)

    print('Successfully created new file with hidden message')
    

def extract(filename):
    file = WaveFile(filename)

    change_sign_samples = int((file.SampleRate / constants.FE_FREQUENCY_TO_EMBED) / 2)
    if change_sign_samples < 1:
        print(f'Sample rate is {file.SampleRate}. Cant extract hidden waves for desired frequency')
        return

    bytes_per_sample = int(file.BitsPerSample / 8)

    channels_positivity = [] # 0 means any, 1 positive, -1 negative
    for _ in range(file.NumChannels):
        channels_positivity.append(Positivity.NEUTRAL)

    data_index = 0

    message = ''
    message_bits = ''

    last_embedded_sample = 0
    current_sample = 0

    while data_index < len(file.data):
        can_extract = True

        for channel in range(file.NumChannels):
            # get over smaller bytes
            data_index += bytes_per_sample - 1

            # we are on significant byte of sample
            positivity = Positivity.POSITIVE if file.data[data_index] < 128 else Positivity.NEGATIVE
            if channels_positivity[channel].value == positivity:
                can_extract = False

            data_index += 1

            channels_positivity[channel] = positivity

        if not can_extract or last_embedded_sample + constants.FE_EMBED_EVERY_SAMPLES > current_sample:
            current_sample += 1
            continue

        for samples_to_swap in [change_sign_samples - 1, change_sign_samples, 1]:
            for _ in range(samples_to_swap):
                for _ in range(file.NumChannels):
                    # if non significan bytes all 8 bits are of message
                    for _ in range(bytes_per_sample - 1):
                        message_bits += bin(file.data[data_index]).lstrip('0b').rjust(8, '0')
                        data_index += 1

                    # if significant byte extract just 7 bits(not most significant)
                    message_bits += bin(file.data[data_index]).lstrip('0b')[-7:].rjust(7, '0')
                    data_index += 1
            
        last_embedded_sample = current_sample
        current_sample += 1

        # try build characters from extracted bits
        while len(message_bits) >= 8:
            character_bits = message_bits[0:8]
            ch = chr(int(character_bits, 2))

            if ch == '#':
                print(f'Successfully extracted the message - {message}')
                return

            message += ch
            message_bits = message_bits[8:]

    print('Couldnt extract the message')