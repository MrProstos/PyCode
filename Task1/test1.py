import time
import psutil
import subprocess
import os
import argparse


def CreateParser():

    parser = argparse.ArgumentParser(
        description="Запуск программы и сбор статистики о ней.")
    parser.add_argument("-b", "--bin", default="/usr/PyCode/foo/bin/python",
                        help="Указать бинарный файл с помощью которого будет запускаться процесс.\nDefault = /usr/bin/python3 ")
    parser.add_argument("-l", "--logfile", default=".",
                        help="Указать путь где будет находиться лог-файл.")
    parser.add_argument("-p", "--path", required=True,
                        help="Обязательно! Путь к исполняемому файлу.")
    parser.add_argument("-t", "--time", default=1,
                        help="Временной интервал записи.")
    return parser


if __name__ == "__main__":
    
    parser = CreateParser()
    namespace = parser.parse_args()

    logfile = namespace.logfile + "/stat.txt"
    bin = namespace.bin
    path = namespace.path
    time_interval = namespace.time

    subp = subprocess.Popen([bin, path])

    p = psutil.Process(subp.pid)

    while True:

        cpu = p.cpu_percent()
        memory = p.memory_info().rss, p.memory_info().vms
        fds = p.num_fds()  # файловые дескрипторы

        stat = """
            Временной интервал: %s 
            Загруска CPU: %s
            Потребление памяти: rss %s и vms %s
            Кол-во файловых дескрипторов: %s
            ----------------------------------------------------""" % (time_interval, cpu, memory[0], memory[1], fds)

        with open(os.path.normpath(logfile), "a") as file:
            file.write(stat)

        time.sleep(time_interval)
