import os
import time
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):

    def process(self, event):
        with open("%s" % os.path.normpath(path_log_file + "/log.txt"), "a") as file:
            file.write("%s %s\n" % (event.src_path, event.event_type))
        print(event.src_path, event.event_type)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)


if __name__ == '__main__':

    try:
        script, path_dir, path_replic_dir, path_log_file, time_interval = sys.argv

        observer = Observer()
        observer.schedule(MyHandler(), path=path_dir, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(int(time_interval))
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    except ValueError:
        err = """
    Недостаточно аргументов для запуска!
    Требуеться указать параметры для запуска:
    path_dir - Путь отслеживаемой директории
    path_replic_dir - Путь хранение реплики отслеживаемой директории
    path_log_file - Путь хранения файла логирования
    time_interval - Врмененной интервал отслеживания

    Пример: /usr/PyCode/Task2/task2.py /usr/PyCode/Task2/TestDir/ /usr/PyCode/ /usr/log/ 1
        """
        print(err)
