import socket

def convert_integer():
    data_32bit = 3579
    data_16bit = 12345
    # 32-bit
    print("original: %s => long host byte order: %s, network byte order: %s" %
          (data_32bit, socket.ntohl(data_32bit), socket.htonl(data_32bit)))
    # 16-bit
    print("original: %s => short host byte order: %s, network byte order: %s" %
          (data_16bit, socket.ntohs(data_16bit), socket.htons(data_16bit)))

if __name__ == '__main__':
    convert_integer()
