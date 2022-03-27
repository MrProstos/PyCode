
import uuid
import socket
import sys

# создаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = ("localhost", 8000)
print("Старт сервера на %s порт %s " % server_address)
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen(50)

while True:
    # ждем соединения
    print("Ожидание соединения...")
    connection, client_address = sock.accept()
    try:
        print("Подключено к:", client_address)
        # Принимаем данные порциями и ретранслируем их
        while True:
            data = connection.recv(1024)
            print(f"Получено: {data.decode()}")
            if data:
                print("Обработка данных...")
                data = str(uuid.uuid4()).encode()
                print("Отправка обратно клиенту.")
                connection.sendall(data)
            else:
                print("Нет данных от:", client_address)
                break

    finally:
        # Очищаем соединение
        connection.close()
