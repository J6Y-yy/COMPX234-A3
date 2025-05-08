import socket
import threading


def handle_client(client_socket):
    pass


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python tuple_space_server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])
    start_server(port)