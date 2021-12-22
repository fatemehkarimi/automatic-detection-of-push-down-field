from .field_usage_listener import FieldUsageListener
from .tree_walker import TreeWalker
from utils.file_reader import FileReader


class FieldUsageExtractor:
    def __init__(self, project_path, project_class_container):
        self.project_path = project_path
        self.class_container = project_class_container

    def extract_field_usage(self):
        for stream in FileReader.get_file_streams(self.project_path):
            listener = FieldUsageListener(self.class_container)
            walker = TreeWalker(listener)
            walker.walk(stream)
            listener = walker.get_listener()
