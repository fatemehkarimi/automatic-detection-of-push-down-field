from .tree_walker import TreeWalker
from .class_extractor_listener import ClassExtractorListener
from utils.file_reader import FileReader


class ClassExtractor:
    def __init__(self, project_path):
        self.project_path = project_path

    def extract_all_classes(self):
        for stream in FileReader.get_file_streams(self.project_path):
            listener = ClassExtractorListener()
            walker = TreeWalker(listener)
            walker.walk(stream)
            listener = walker.get_listener()
