import socket
import threading
import time


tuple_space = {}
client_count = 0
operation_count = 0
read_count = 0
get_count = 0
put_count = 0
error_count = 0


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
    global client_count, operation_count, read_count, get_count, put_count, error_count
    client_count += 1
    try:
        request = client_socket.recv(1024).decode()
        command, key, value = decode_request(request)
        operation_count += 1
        if command == 'P':
            put_count += 1
            if key in tuple_space:
                response = "ERR {} already exists".format(key)
                error_count += 1
            else:
                tuple_space[key] = value
                response = "OK ({} , {}) added".format(key, value)
        elif command == 'R':
            read_count += 1
            if key in tuple_space:
                response = "OK ({} , {}) read".format(key, tuple_space[key])
            else:
                response = "ERR {} does not exist".format(key)
                error_count += 1
        elif command == 'G':
            get_count += 1
            if key in tuple_space:
                removed_value = tuple_space.pop(key)
                response = "OK ({} , {}) removed".format(key, removed_value)
            else:
                response = "ERR {} does not exist".format(key)
                error_count += 1
        encoded_response = encode_response(response)
        client_socket.sendall(encoded_response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
        error_count += 1
    finally:
        client_socket.close()


def print_server_status():
    global client_count, operation_count, read_count, get_count, put_count, error_count
    while True:
        time.sleep(10)
        tuple_count = len(tuple_space)
        if tuple_count > 0:
            total_tuple_size = sum(len(key) + len(value) for key, value in tuple_space.items())
            average_tuple_size = total_tuple_size / tuple_count
            average_key_size = sum(len(key) for key in tuple_space.keys()) / tuple_count
            average_value_size = sum(len(value) for value in tuple_space.values()) / tuple_count
        else:
            average_tuple_size = 0
            average_key_size = 0
            average_value_size = 0
        print(f"Tuple space status:")
        print(f"Number of tuples: {tuple_count}")
        print(f"Average tuple size: {average_tuple_size}")
        print(f"Average key size: {average_key_size}")
        print(f"Average value size: {average_value_size}")
        print(f"Total clients connected: {client_count}")
        print(f"Total operations: {operation_count}")
        print(f"Total READs: {read_count}")
        print(f"Total GETs: {get_count}")
        print(f"Total PUTs: {put_count}")
        print(f"Total errors: {error_count}")


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    status_thread = threading.Thread(target=print_server_status)
    status_thread.daemon = True
    status_thread.start()

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