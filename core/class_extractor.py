from .tree_walker import TreeWalker
from .class_extractor_listener import ClassExtractorListener
from utils.container import Container
from utils.file_reader import FileReader


class ClassExtractor:
    def __init__(self, project_path):
        self.project_path = project_path
        self.project_class_container = Container()

    def extract_all_classes(self):
        for stream in FileReader.get_file_streams(self.project_path):
            listener = ClassExtractorListener()
            walker = TreeWalker(listener)
            walker.walk(stream)
            listener = walker.get_listener()
            class_container = listener.get_class_container()
            for j_class in class_container.element_list():
                self.project_class_container.add_element(j_class)

    def get_project_classes(self):
        return self.project_class_container
