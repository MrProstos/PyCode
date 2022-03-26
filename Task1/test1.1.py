import time
import psutil
import subprocess
import os


def _main():

    print("В какой директории хранить лог-файл")
    logfile = str(input()) + "/stat.txt"

    print("Введи путь до процесса который нужно запустить")
    path = str(input())

    print("Введите временной интервал сканирования в секундах")
    time_interval = int(input())

    subp = subprocess.Popen(["/usr/PyCode/foo/bin/python",
                            "/usr/PyCode/Task1/Task1Test/test1.1.py"])

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
        print(time_interval, cpu, memory[0], memory[1], fds)

        with open(os.path.normpath(logfile), "a") as file:
            file.write(stat)

        time.sleep(time_interval)


if __name__ == "__main__":
    _main()
