import wave
import soundfile as sf


def hide(input_filename, output_filename, secret):
    ob = sf.SoundFile(input_filename)
    song = wave.open(input_filename, mode='rb')

    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in secret])))

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit

    frame_modified = bytes(frame_bytes)

    with wave.open(output_filename, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    song.close()

def extract(filename):
    song = wave.open(filename, mode='rb')

    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    decoded = string.split("#")[0]

    print("Sucessfully decoded: " + decoded)
    song.close()