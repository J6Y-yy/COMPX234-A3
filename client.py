import socket


def send_request(host, port, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response


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