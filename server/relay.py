import socket
import select

class server:
    def __init__(self, ip, port, listen_queue=2):
        self.ip = ip
        self.port = port
        self.listen_queue = listen_queue
        self.client_sockets = {}  # сокет -> (IP, порт)
        self.sock = None

    def send_msg(self, msg, client):
        client.sendall(msg)

    def listner(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(self.listen_queue)

        self.is_work = True
        print("жду подключения на", self.sock.getsockname())

        while self.is_work:
            sockets_to_check = [self.sock] + list(self.client_sockets)
            result = select.select(sockets_to_check, [], [], 0.5)
            ready_sockets = result[0]

            for current_socket in ready_sockets:
                if current_socket == self.sock:
                    client_socket, client_addr = self.sock.accept()
                    self.client_sockets[client_socket] = client_addr
                    print(f"клиент подключен\n\t{client_addr}")
                    continue

                if current_socket not in self.client_sockets:
                    continue

                try:
                    data = current_socket.recv(1024)
                except OSError:
                    self.disconnect_client(current_socket)
                    continue

                if data == b"":
                    self.disconnect_client(current_socket)
                    continue

                # Список нужен, чтобы можно было удалить сокет при ошибке отправки.
                for client_socket in list(self.client_sockets):
                    if client_socket != current_socket:
                        try:
                            self.send_msg(data, client_socket)
                        except OSError:
                            self.disconnect_client(client_socket)

    def disconnect_client(self, client_socket):
        client_addr = self.client_sockets[client_socket]
        del self.client_sockets[client_socket]
        client_socket.close()
        print("клиент отключился:", client_addr)

    def close(self):
        self.is_work = False
        for client_socket in list(self.client_sockets):
            self.disconnect_client(client_socket)
        if self.sock is not None:
            self.sock.close()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5001
    listen_queue = 2

    app = server(ip, port, listen_queue)
    try:
        app.listner()
    except KeyboardInterrupt:
        print("\nсервер остановлен")
    except OSError as error:
        print("ошибка сервера:", error)
    app.close()
