import socket
import sys
import argparse
import select


host = '0.0.0.0'
data_payload = 32
backlog = 1

def get_in_addr(sa):
    """Mengembalikan alamat IP berdasarkan IPv4 atau IPv6."""
    if sa.family == socket.AF_INET:
        return sa[0]
    else:
        return sa[0]

def echo_server(port):
    """Server TCP yang menangani banyak klien menggunakan select() dan echo data kembali ke klien."""
    # Membuat TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mengizinkan reuse alamat/port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind socket ke port
    server_address = (host, port)
    print(f"Starting up echo server on {server_address[0]} port {server_address[1]}")
    server_socket.bind(server_address)

    # Listen untuk klien, backlog menentukan berapa banyak koneksi yang bisa dikelola dalam antrian
    server_socket.listen(backlog)
    print(f"Server listening on {host}:{port} with backlog {backlog}")

    # Menggunakan select untuk menangani banyak klien
    master = [server_socket]  # Daftar file descriptor yang dimonitor
    fdmax = server_socket.fileno()  # Menyimpan nilai file descriptor terbesar

    while True:
        read_fds, _, _ = select.select(master, [], [])

        for sock in read_fds:
            if sock is server_socket:
                # Menerima koneksi baru
                client_socket, client_address = server_socket.accept()
                master.append(client_socket)
                fdmax = max(fdmax, client_socket.fileno())
                print(f"New connection from {client_address[0]} on socket {client_socket.fileno()}")
            else:
                # Menerima data dari klien yang sudah terhubung
                try:
                    data = sock.recv(data_payload)
                    if data:
                        print(f"Data received from {sock.getpeername()}: {data.decode('utf-8')}")
                        # Mengirim balik data ke klien (echo)
                        sock.send(data)
                        print(f"Sent {len(data)} bytes back to {sock.getpeername()}")
                    else:
                        # Jika tidak ada data, koneksi tertutup
                        print(f"Connection closed by {sock.getpeername()}")
                        master.remove(sock)
                        sock.close()
                except Exception as e:
                    print(f"Error: {e}")
                    master.remove(sock)
                    sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket server example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)

    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
