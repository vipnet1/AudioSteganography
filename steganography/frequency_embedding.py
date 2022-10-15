from tools.wave_file import WaveFile
import tools.arguments_parser as arguments_parser
import core.constants as constants
from enums.positivity import Positivity
import core.common as common

def hide(filename):
    message = arguments_parser.parse_message()

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

    data_index = 0
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

        if not can_embed:
            continue

    file.replace_data_block(new_data)

    output_filename = common.get_output_filename('lsb_basic')
    file.save_file(output_filename)

    print('yo')
    

def extract(filename):
    pass