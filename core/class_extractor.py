from .tree_walker import TreeWalker
from .class_extractor_listener import ClassExtractorListener
from utils.container import Container
from utils.file_reader import FileReader


class ClassExtractor:
    def __init__(self, project_path):
        self.project_path = project_path
        self.project_class_container = Container()

    def set_parent_objects(self):
        for j_class in self.project_class_container.element_list():
            for parent_identifier in j_class.parent_identifiers:
                parent_class = self.project_class_container.get_element_by_identifier(parent_identifier)
                if parent_class:
                    j_class.add_parent(parent_class)

    def set_children_objects(self):
        for j_class in self.project_class_container.element_list():
            for parent_class in j_class.parent_list():
                parent_class.add_child(j_class)

    def extract_all_classes(self):
        for stream in FileReader.get_file_streams(self.project_path):
            listener = ClassExtractorListener()
            walker = TreeWalker(listener)
            walker.walk(stream)
            listener = walker.get_listener()
            class_container = listener.get_class_container()
            for j_class in class_container.element_list():
                self.project_class_container.add_element(j_class)
        self.set_parent_objects()
        self.set_children_objects()

    def get_project_classes(self):
        return self.project_class_container
