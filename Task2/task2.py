import os
import argparse
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):

    def process(self, event): # функция записи в лог файл
        with open("%s" % os.path.normpath(path_log_file + "/log_replic.txt"), "a") as file:
            file.write("%s %s %s\n" %
                       (time.asctime(), event.src_path, event.event_type))

        print(time.asctime(), event.src_path, event.event_type)

    def mod_path(self, event): # изменение строки для получения пути куда нужно сохранять реплику  
        mod_file = str(event.src_path).partition(
            os.path.basename("/"+os.path.dirname(path_dir)))[1:]

        return path_replic_dir + mod_file[0] + mod_file[1]

    def on_modified(self, event):
        self.process(event)
        if not event.is_directory:
            os.system("cp %s %s" % (event.src_path, self.mod_path(event)))

    def on_created(self, event):
        self.process(event)
        if event.is_directory:
            os.system("cp -r %s %s" % (event.src_path, self.mod_path(event)))
        else:
            os.system("cp %s %s" % (event.src_path, self.mod_path(event)))

    def on_deleted(self, event):
        self.process(event)
        if event.is_directory:
            os.system("rm -r %s" % self.mod_path(event))
        else:
            os.system("rm %s" % self.mod_path(event))


def CreateParser():
    parser = argparse.ArgumentParser(
        description="Запуск программы для отслеживания изменений в каталоге.")
    parser.add_argument("-p", "--path_dir", required=True,
                        help="Укажите путь отслеживаемой директории.Обязательно!")
    parser.add_argument("-l", "--path_log_file", default=".",
                        help="Указать путь где будет находиться лог-файл.")
    parser.add_argument("-r", "--path_replic_dir", required=True,
                        help="Путь где будет храниться реплика.Обязательно!")
    parser.add_argument("-t", "--time_interval", default=1,
                        help="Временной интервал записи.")
    return parser


if __name__ == '__main__':

    parser = CreateParser()
    namespace = parser.parse_args()

    path_dir = namespace.path_dir
    path_replic_dir = namespace.path_replic_dir
    path_log_file = namespace.path_log_file
    time_interval = namespace.time_interval

    if os.path.exists(path_replic_dir):
        os.system("cp -r %s %s" % (path_dir, path_replic_dir))

    observer = Observer(timeout=time_interval)
    observer.schedule(MyHandler(), path=path_dir,
                      recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
