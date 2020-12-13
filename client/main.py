import socket

from models.request_router import RequestRouter

HOST, PORT = '0.0.0.0', 8080


def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((HOST, PORT))
        listen_socket.listen()
        print(f'Start serving on port {PORT}')
        while client := listen_socket.accept():
            connection = client[0]
            router = RequestRouter()
            with connection:
                while request := connection.recv(1024):
                    if request[-1:] == b'\n':
                        request = request[:-1]
                    if request[-1:] == b'\r':
                        request = request[:-1]
                    try:
                        decoded_request = request.decode()
                    except UnicodeDecodeError:
                        connection.sendall(b'Unicode decode error\n')
                        break
                    if decoded_request == 'QUIT':
                        break
                    response = router.route_request(decoded_request) + '\n'
                    connection.sendall(response.encode())
        print('End serving')


if __name__ == '__main__':
    serve()
