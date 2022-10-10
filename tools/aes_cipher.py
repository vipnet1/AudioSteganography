from hashlib import md5
from base64 import b64decode, b64encode

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

# public_key = aes_cipher.generate_key()
public_key = b'\x9b\xda\xeaH\xec\x98\xda\x9f\xf8Lw\x1d&\xc2X\x8a'

def encrypt(key, data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(pad(data, AES.block_size)))

def decrypt(key, data):
    raw = b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, raw[:AES.block_size])
    return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)

def generate_key():
    random_data = get_random_bytes(30)
    key = md5(random_data).digest()
    return key