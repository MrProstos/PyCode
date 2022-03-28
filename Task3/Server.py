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

    def msg_write(self, text: list):
        try:
            print(unique_data)
            for i in unique_data:
                for key, value in i.items():
                    print(key, text[0], value, text[1])
                    if key == text[0] and value == text[1]:
                        with open("log_server.txt", "a") as file:
                            file.write("%s %s %s\n" %
                                       (time.asctime(), text[0:2], text[2]))
                        return "Успех! Данные подтверждены."

            return "Ошибка! Неправильные данные."
        except IndexError:
            return "Ошибка! Введене не полный объем данных"

    def server1_run(self):

        while True:
            # ждем соединения
            print("(Порт 8000) Ожидание соединения...")

            connection, client_address = self.sock.accept()

            try:
                print("Подключено к:", client_address)

                while True:
                    identifier = connection.recv(2048)
                    print("Получено: %s" % identifier.decode())
                    if identifier:
                        print("Обработка данных...")
                        msg = str(uuid.uuid4()).encode()
                        user_info = {"%s" % identifier.decode(): "%s" %
                                     msg.decode()}

                        if len(unique_data) > 50:
                            unique_data.remove(unique_data[0])

                        unique_data.append(user_info)
                        print("Отправка обратно клиенту.")
                        connection.sendall(msg)

                    else:
                        print("Нет данных от:", client_address)
                        break

            finally:
                connection.close()

    def server2_run(self):

        while True:

            print("(Порт 8001) Ожидание соединения...")
            connection, client_address = self.sock.accept()
            try:
                print("Подключено к:", client_address)
                while True:
                    msg = connection.recv(2048)
                    print("Получено %s" % msg.decode())
                    if msg:
                        connection.send(self.msg_write(
                            msg.decode().split(" ")).encode())

                    else:
                        print("Нет данных")
                        break
            finally:
                connection.close()


if __name__ == '__main__':

    unique_data = []

    ports = [8000, 8001]

    for port in ports:

        if port == 8000:
            thread1 = threading.Thread(
                target=Socket_server("localhost", port).server1_run)
            thread1.start()

        if port == 8001:
            thread2 = threading.Thread(
                target=Socket_server("localhost", port).server2_run)
            thread2.start()
