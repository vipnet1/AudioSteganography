import core.constants as constants
from datetime import datetime
import base64

def get_output_filename(tag):
    filename = f'{constants.OUTPUT_FILE_PREFIX}_{tag}_{datetime.now()}.wav'
    return filename.replace(' ', '_').replace(':', '_')

def get_personal_key_filename(tag):
    filename = f'{constants.OUTPUT_KEY_PREFIX}_{tag}_{datetime.now()}.key'
    return filename.replace(' ', '_').replace(':', '_')

def to_base64(the_string):
    b64_bytes = base64.b64encode(bytes(the_string, 'utf-8')) # bytes
    return b64_bytes.decode('utf-8')

def from_base64(base64_string):
    string_bytes = base64.b64decode(base64_string)
    return string_bytes.decode('utf-8')