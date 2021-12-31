from .field_usage_listener import FieldUsageListener
from .tree_walker import TreeWalker
from utils.file_reader import FileReader


class FieldUsageExtractor:
    def __init__(self, project_path, project_class_container):
        self.project_path = project_path
        self.class_container = project_class_container

    def extract_external_field_usage(self, class_field_usage):
        for class_name, field_name in class_field_usage:
            if self.class_container.has_element(class_name):
                j_class = self.class_container.get_element_by_identifier(class_name)
                class_fields = j_class.get_field_container()
                if class_fields.has_element(field_name):
                    field = class_fields.get_element_by_identifier(field_name)
                    j_class.add_used_field(field)

    def extract_field_usage(self):
        class_field_usage = []
        for stream in FileReader.get_file_streams(self.project_path):
            listener = FieldUsageListener(self.class_container)
            walker = TreeWalker(listener)
            walker.walk(stream)
            listener = walker.get_listener()
            class_field_usage.extend(listener.get_class_field_usage())
        self.extract_external_field_usage(class_field_usage)
