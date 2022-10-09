import wave

def lsb_hide(src_filename, dest_filename, secret):
    # read wave audio file
    song = wave.open(src_filename, mode='rb')

    # Read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    string = secret

    # Append dummy data to fill out rest of the bytes.
    string = string + int(len(frame_bytes) - len(string) * 8) * '#'

    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit

    # Get the modified bytes
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    with wave.open(dest_filename, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    song.close()

    print(f'Successfully hide secret inside file {dest_filename}')

def lsb_extract(filename):
    song = wave.open(filename, mode='rb')

    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded: "+decoded)

    song.close()

lsb_hide('song.wav', 'song_embedded.wav', 'Hi Im Timur')