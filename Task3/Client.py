import socket
import sys

# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаем сокет к порту, через который прослушивается сервер
server_address = ("localhost", 8000)
print("Подключено к {} порт {}".format(*server_address))


print("Введите свой уникальный идентификатор")
identificator = str(input())

sock.connect(server_address)

try:
    # Отправка данных
    mess = identificator
    print(f"Отправка: {mess}")
    message = mess.encode()
    sock.sendall(message)

    # Смотрим ответ
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        unique_code = data.decode()
        print("Получено: %s" % data.decode())

    #server_address = ("localhost",8001)

    
finally:
    print("Закрываем сокет")
    sock.close()
