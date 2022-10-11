import tools.arguments_parser as arguments_parser
from tools.wave_file import WaveFile
import core.common as common
import core.constants as constants

def hide(filename):
    message = arguments_parser.parse_message()

    file = WaveFile(filename)

    # samples count for embedded wave to be on correct frequency
    samples_count = int((float(file.SampleRate) / constants.FREQUENCY_TO_HIDE_ON) / 2)
    if samples_count == 0:
        print('Too small sample rate - cant embed waves with correct frequency')
        return

    for index in range(len(file.data)):
        mod_res = index % 8
        if mod_res == 0 or mod_res == 2:
            file.data[index] = 0
        elif mod_res == 1 or mod_res == 3:
            file.data[index] = 10
        elif mod_res == 4 or mod_res == 6:
            file.data[index] = 0
        elif mod_res == 5 or mod_res == 7:
            file.data[index] = 250

    file.save_file('rito.wav')
    print('yo')

def extract(filename):
    pass