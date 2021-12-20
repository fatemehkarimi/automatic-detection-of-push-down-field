import os
from antlr4 import *


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def get_file_stream(cls, file):
        try:
            stream = FileStream(file, encoding='utf-8')
        except UnicodeDecodeError:
            stream = FileStream(file, encoding='latin-1')
        return stream

    @staticmethod
    def get_file_streams(cls, path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file() and entry.name.endswith('.java'):
                    yield cls.get_file_stream(entry.path)
                elif entry.is_dir():
                    yield from cls.get_file_streams(entry.path)
