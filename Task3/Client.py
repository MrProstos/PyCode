import socket
import sys


class Socket_client():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Client1(self):
        try:
            identificator = str(
                input("Введите свой уникальный идентификатор\n"))

            self.sock.connect((self.ip, self.port))
            print("Отправка %s" % identificator)

            encode_identificator = identificator.encode()
            self.sock.sendall(encode_identificator)

            amount_received = 0
            amount_expected = len(encode_identificator)
            while amount_received < amount_expected:
                data = self.sock.recv(1024)
                amount_received += len(data)
                unique_code = data.decode()

        finally:
            print("Идентификатор - %s, уникальный код - %s" %
                  (identificator, unique_code))
            print("Закрываем сокет")
            self.sock.close()

    def Client2(self):
        
        try:
            msg_text = str(input("Введите свой идентификатор и уникальный код"))
            text = str(input("Введите текст произвольной длинный"))
         
            self.sock.connect((self.ip,self.port))
            
        
        finally:
            self.sock.close()


if __name__ == "__main__":
    s = Socket_client("localhost", 8000)
    s.Client1()
