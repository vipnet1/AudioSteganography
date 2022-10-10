import tools.arguments_parser as arguments_parser
from tools.wave_file import WaveFile
import core.common as common

def hide(filename):
    message = arguments_parser.parse_message()
    file = WaveFile(filename)

    output_filename = common.get_output_filename()
    file.save_file(output_filename)
    

def extract(filename):
    pass