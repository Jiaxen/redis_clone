import socket  # noqa: F401
import concurrent.futures

from app.redis_service import RedisService

THREADS = 5
CHUNK_SIZE = 1024
DB = {}

def main():
    print("Starting redis clone server")

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
        while True:
            client_socket, address = server_socket.accept() # wait for client
            executor.submit(handle_client, client_socket)

def handle_client(client_socket):
    rs = RedisService(DB)
    while True:
        data_chunk = client_socket.recv(CHUNK_SIZE)
        if not data_chunk:
            break
        client_socket.sendall(rs.handle_request(data_chunk))
    client_socket.close()


if __name__ == "__main__":
    main()
