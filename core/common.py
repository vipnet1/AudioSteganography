import core.constants as constants
from datetime import datetime

def get_output_filename():
    filename = f'{constants.OUTPUT_FILE_PREFIX}{datetime.now()}.wav'
    return filename.replace(' ', '_').replace(':', '_')