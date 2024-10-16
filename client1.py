import socket
import sys


def chat_client():
    """Client TCP sederhana yang bisa berinteraksi dengan server"""
    # Input dari pengguna untuk IP server dan port server
    server_ip = input("Masukkan IP server: ")
    server_port = int(input("Masukkan port server: "))

    # Membuat socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Menghubungkan ke server
    server_address = (server_ip, server_port)
    print("Menghubungkan ke %s port %s" % server_address)

    try:
        sock.connect(server_address)
        print("Koneksi berhasil")

        while True:
            # Mengirim pesan ke server
            message = input("Client (ketik pesan): ")
            sock.sendall(message.encode('utf-8'))

            # Menerima balasan dari server
            data = sock.recv(1024).decode('utf-8')
            print(f"Pesan dari server: {data}")

    except Exception as e:
        print(f"Gagal koneksi atau terjadi kesalahan: {e}")

    finally:
        # Menutup koneksi
        print("Koneksi ditutup")
        sock.close()


if __name__ == '__main__':
    chat_client()
