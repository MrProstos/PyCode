import socket
import threading
import uuid
import time


class Socket_server():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(50)

    def msg_write(self, msg: dict, *text: str):
        for key, value in unique_data.items():
            for msg_key, msg_value in msg.items():
                if key == msg_key and value == msg_value:
                    print("УСПЕХ!")
                    with open("/log.txt", "a") as file:
                        file.write("%s %s %s" % (time.asctime(), msg, text))

    def server1_run(self):

        while True:
            # ждем соединения
            print("(Порт 8000) Ожидание соединения...")

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

                    else:
                        print("Нет данных от:", client_address)
                        break

            finally:
                connection.close()

    def server2_run(self):

        while True:

            print("Ожидание соединения сервер 2...")
            connection, client_address = self.sock.accept()
            try:
                print("Подключено к:", client_address)
                while True:
                    msg = connection.recv(1024)
                    print("Получено %s" % msg.decode())
                    if msg:
                        print("Сообщение есть")

                    else:
                        print("Нет данных")
                        break
            finally:
                # Очищаем соединение
                connection.close()


if __name__ == '__main__':

    unique_data = {}

    ports = [8000, 8001]

    for port in ports:

        s = Socket_server("localhost", port)

        if port == 8000:
            thread1 = threading.Thread(target=s.server1_run())
            thread1.start()

        if port == 8001:
            thread2 = threading.Thread(target=s.server2_run())
            thread2.start()
