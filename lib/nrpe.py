'''

typedef struct packet_struct {
int16_t packet_version;
int16_t packet_type;
uint32_t crc32_value;
int16_t result_code;
char buffer[1024];
} packet;



'''

import struct
import zlib


PACKET_FORMAT = "!HHIH1024s2s"

class NrpePacket(object):
    def __init__(self, buffer , version=2, type=1, result_code=0, lb='\x00\x00'):
        '''
        NRPE Packet, CRC32 is auto-calculated.
        :param version: version number.
        :param type: Type. 1 for Query, 2 for Response
        :param result_code: code similar to "exit code" 0 for ok, 1 for warning, 2 for critical, etc.
        :param buffer: message. the nrpe command.
        '''
        self.__ver = version;
        self.__type = type;
        self.__result = result_code;
        self.__buffer = buffer;
        self.__lb = lb
        #compute crc32
        crc = zlib.crc32(struct.pack(PACKET_FORMAT, self.__ver, self.__type, 0, self.__result, self.__buffer, self.__lb));
        #unsigned
        crc = crc & 0xffffffff

        self.__crc = crc;

    @property
    def data(self):
        packet = struct.pack(PACKET_FORMAT, self.__ver, self.__type, self.__crc, self.__result, self.__buffer, self.__lb);
        return packet;

    @property
    def crc(self):
        return self.__crc
