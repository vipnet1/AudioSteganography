# wave file format doc http://soundfile.sapp.org/doc/WaveFormat/
class WaveFile:
    def __init__(self, filename):
        self.filename = filename
        self.__parse_raw_data()
        self.__store_info()
        self.__perform_validations()

    # use if also size of data block changed, else posssible just to work directly with self.data
    def replace_data_block(self, new_data):
        diff_num = len(new_data) - len(self.data)

        self.data = new_data
        self.ChunkSize += diff_num
        self.Subchunk2Size += diff_num

        self.__r_data = bytes(new_data)
        self.__r_ChunkSize = self.ChunkSize.to_bytes(4, 'little')
        self.__r_Subchunk2Size = self.Subchunk2Size.to_bytes(4, 'little')

    def save_file(self, dest_file):
        bin_data = self.__r_ChunkID + self.__r_ChunkSize + self.__r_Format + self.__r_Subchunk1ID + \
                   self.__r_Subchunk1Size + self.__r_AudioFormat + self.__r_NumChannels + self.__r_SampleRate + \
                   self.__r_ByteRate + self.__r_BlockAlign + self.__r_BitsPerSample + self.__r_Subchunk2ID + \
                   self.__r_Subchunk2Size + bytes(self.data)

        with open(dest_file, 'wb') as file:
            file.write(bin_data)

    def __parse_raw_data(self):
        with open(self.filename, mode='rb') as file:
            fileContent = file.read()

            self.__fileContent = fileContent
            self.__r_ChunkID = fileContent[0:4]
            self.__r_ChunkSize = fileContent[4:8]
            self.__r_Format = fileContent[8:12]
            self.__r_Subchunk1ID = fileContent[12:16]
            self.__r_Subchunk1Size = fileContent[16:20]
            self.__r_AudioFormat = fileContent[20:22]
            self.__r_NumChannels = fileContent[22:24]
            self.__r_SampleRate = fileContent[24:28]
            self.__r_ByteRate = fileContent[28:32]
            self.__r_BlockAlign = fileContent[32:34]
            self.__r_BitsPerSample = fileContent[34:36]
            self.__r_Subchunk2ID = fileContent[36:40]
            self.__r_Subchunk2Size = fileContent[40:44]
            self.__r_data = fileContent[44:]

    def __store_info(self):
        self.ChunkSize = int.from_bytes(self.__r_ChunkSize, byteorder='little', signed=False)
        self.Subchunk1Size = int.from_bytes(self.__r_Subchunk1Size, byteorder='little', signed=False)
        self.AudioFormat = int.from_bytes(self.__r_AudioFormat, byteorder='little', signed=False)
        self.NumChannels = int.from_bytes(self.__r_NumChannels, byteorder='little', signed=False)
        self.SampleRate = int.from_bytes(self.__r_SampleRate, byteorder='little', signed=False)
        self.ByteRate = int.from_bytes(self.__r_ByteRate, byteorder='little', signed=False)
        self.BlockAlign = int.from_bytes(self.__r_BlockAlign, byteorder='little', signed=False)
        self.BitsPerSample = int.from_bytes(self.__r_BitsPerSample, byteorder='little', signed=False)
        self.Subchunk2Size = int.from_bytes(self.__r_Subchunk2Size, byteorder='little', signed=False)
        self.data = bytearray(self.__r_data)

    def __perform_validations(self):
        self.problems = ''

        if self.ChunkSize != len(self.__fileContent) - 8:
            self.problems += 'Invalid file size - file may be corrupted|'

        expectedByteRate = self.SampleRate * self.NumChannels * self.BitsPerSample / 8;
        if expectedByteRate != self.ByteRate:
            self.problems += 'Invalid byte rate|'

        expectedBlockAlign = self.NumChannels * self.BitsPerSample / 8;
        if expectedBlockAlign != self.BlockAlign:
            self.problems += 'Invalid block align|'

        if self.AudioFormat != 1:
            self.problems += 'Not PCM file - probably compressed. Are you sure its a WAV file?|'