import socket
import threading
import uuid


class socket_server():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(50)

    def server1_run(self):

        while True:
            # ждем соединения
            print("Ожидание соединения сервер 1...")

            connection, client_address = self.sock.accept()
            try:
                print("Подключено к:", client_address)
                # Принимаем данные порциями и ретранслируем их
                while True:
                    identifier = connection.recv(1024)
                    print("Получено: %s" % identifier.decode())
                    if identifier:
                        print("Обработка данных...")
                        msg = str(uuid.uuid4()).encode()
                        a = {"%s" % identifier.decode(): "%s" % msg.decode()}
                        unique_data.update(a)
                        print("Отправка обратно клиенту.")

                        connection.sendall(msg)
                        connection.sendall(str(a).encode())

                        print(unique_data)
                    else:
                        print("Нет данных от:", client_address)
                        break

            finally:
                # Очищаем соединение
                connection.close()

    def server2_run(self):

        while True:

            # ждем соединения
            print("Ожидание соединения сервер 2...")
            connection, client_address = self.sock.accept()
            try:
                print("Подключено к:", client_address)
                # Принимаем данные порциями и ретранслируем и

            finally:
                # Очищаем соединение
                connection.close()


if __name__ == '__main__':

    unique_data = {}

    ports = [8000, 8001]

    for port in ports:

        s = socket_server("localhost", port)

        if port == 8000:
            thread1 = threading.Thread(target=s.server1_run())
            thread1.start()

        if port == 8001:
            thread2 = threading.Thread(target=s.server2_run())
            thread2.start()
