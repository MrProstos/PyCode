import os
import time
import sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):

    def process(self, event):
        with open("%s" % os.path.normpath(path_log_file + "/log.txt"), "a") as file:
            file.write("%s %s %s\n" %
                       (time.asctime(), event.src_path, event.event_type))

        print(time.asctime(), event.src_path, event.event_type)

    def mod_path(self, event):
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
            os.system("cp -r %s %s" %( event.src_path, self.mod_path(event)))
        else:
            os.system("cp %s %s" %( event.src_path, self.mod_path(event)))

    def on_deleted(self, event):
        self.process(event)
        os.system("rm %s" % self.mod_path(event))


if __name__ == '__main__':

    try:
        _, path_dir, path_replic_dir, path_log_file, time_interval = sys.argv

        if os.path.exists(path_replic_dir):
            os.system("cp -r %s %s" % (path_dir, path_replic_dir))

        observer = Observer()
        observer.schedule(MyHandler(), path=path_dir,
                          recursive=True)
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
