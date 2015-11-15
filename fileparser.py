import os


def directory_decorate(func):
    def func_wrapper(self, *args, **kwargs):
        self.go_to_directory()
        result = func(self, *args, **kwargs)
        self.reset_original_directory()
        return result
    return func_wrapper


def format_path(path):
    if path:
        return "./" + path
    else:
        return "./"


class FileParser:

    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.original_directory = ""

    def go_to_directory(self):
        self.original_directory = os.getcwd()
        os.chdir(self.directory_path)

    def reset_original_directory(self):
        os.chdir(self.original_directory)

    @directory_decorate
    def list_file(self, path=None):
        return os.listdir(format_path(path))

    @directory_decorate
    def walk_torrent(self, path=None):
        return os.walk(os.getcwd())
