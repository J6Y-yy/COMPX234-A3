import socket


def encode_request(request):
    parts = request.split()
    if parts[0] == 'PUT':
        total_size = len(request) + 3
        msg = f"{total_size:03d} P {' '.join(parts[1:])}"
    elif parts[0] == 'READ':
        total_size = len(request) + 3
        msg = f"{total_size:03d} R {parts[1]}"
    elif parts[0] == 'GET':
        total_size = len(request) + 3
        msg = f"{total_size:03d} G {parts[1]}"
    else:
        raise ValueError("Invalid request command")
    return msg


def decode_response(response):
    return response[3:].strip()


def send_request(host, port, request):
    encoded_request = encode_request(request)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(encoded_request.encode())
    response = client_socket.recv(1024).decode()
    decoded_response = decode_response(response)
    client_socket.close()
    return decoded_response


def process_request_file(host, port, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                response = send_request(host, port, line)
                print(f"{line}: {response}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python tuple_space_client.py <host> <port> <file_path>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    process_request_file(host, port, file_path)