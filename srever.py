import socket
import threading


def decode_request(request):
    total_size = int(request[:3])
    command = request[3]
    if command == 'P':
        parts = request[4:].split(' ', 1)
        key = parts[0]
        value = parts[1] if len(parts) > 1 else ''
    elif command in ['R', 'G']:
        key = request[4:]
        value = ''
    else:
        raise ValueError("Invalid request command")
    return command, key, value


def encode_response(response):
    total_size = len(response) + 3
    return f"{total_size:03d} {response}"


def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        command, key, value = decode_request(request)
        # 这里暂未实现具体操作，仅返回示例响应
        if command == 'P':
            response = "OK ({} , {}) added".format(key, value)
        elif command == 'R':
            response = "OK ({} , {}) read".format(key, 'example_value')
        elif command == 'G':
            response = "OK ({} , {}) removed".format(key, 'example_value')
        encoded_response = encode_response(response)
        client_socket.sendall(encoded_response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


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