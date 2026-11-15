import socket

class client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.ip, self.port))

    def send_msg(self, msg):
        self.sock.sendall(msg)

    def receive_msg(self):
        data = self.sock.recv(1024)
        return data

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5001
    app = client(ip, port)

    try:
        app.connect()
        print("подключился к серверу")
        print("1 — отправить, 2 — получить, 0 — выйти")

        while True:
            action = input("действие: ")

            if action == "0":
                break

            if action == "1":
                msg = input("сообщение: ")
                data = msg.encode('utf-8')
                app.send_msg(data)

            if action == "2":
                data = app.receive_msg()
                if data == b"":
                    print("сервер отключился")
                    break
                msg = data.decode('utf-8', errors='replace')
                print("получено:", msg)
    except KeyboardInterrupt:
        print("\nклиент остановлен")
    except EOFError:
        print("ввод завершён")
    except OSError as error:
        print("ошибка соединения:", error)
    app.close()
