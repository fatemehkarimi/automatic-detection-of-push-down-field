from .field_usage_extractor import FieldUsageExtractor
from .class_extractor import ClassExtractor
from utils.container import Container

class PushDownFieldDetector:
    def __init__(self, project_path):
        self.project_path = project_path
        self.project_class_container = Container()

    def extract_project_classes(self):
        class_extractor = ClassExtractor(self.project_path)
        class_extractor.extract_all_classes()
        self.project_class_container = class_extractor.get_project_classes()

    def extract_field_usage(self):
        field_usage_extractor = FieldUsageExtractor(self.project_path, self.project_class_container)
        field_usage_extractor.extract_field_usage()
