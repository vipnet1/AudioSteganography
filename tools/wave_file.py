# wave file format doc http://soundfile.sapp.org/doc/WaveFormat/
class WaveFile:
    def __init__(self, filename):
        self.filename = filename
        self.__parse_raw_data()
        self.__store_info()
        self.__perform_validations()

    def save_file(self, dest_file):
        bin_data = self.__r_ChunkID + self.__r_ChunkSize + self.__r_Format + self.__r_Subchunk1ID + \
                   self.__r_Subchunk1Size + self.__r_AudioFormat + self.__r_NumChannels + self.__r_SampleRate + \
                   self.__r_ByteRate + self.__r_BlockAlign + self.__r_BitsPerSample + self.__r_Subchunk2ID + \
                   self.__r_Subchunk2Size + self.r_data

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
            self.r_data = fileContent[44:]

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

    def __perform_validations(self):
        self.__problems = ''

        if self.ChunkSize != len(self.__fileContent) - 8:
            self.__problems += 'Invalid file size - file may be corrupted|'

        expectedByteRate = self.SampleRate * self.NumChannels * self.BitsPerSample / 8;
        if expectedByteRate != self.ByteRate:
            self.__problems += 'Invalid byte rate|'

        expectedBlockAlign = self.NumChannels * self.BitsPerSample / 8;
        if expectedBlockAlign != self.BlockAlign:
            self.__problems += 'Invalid block align|'