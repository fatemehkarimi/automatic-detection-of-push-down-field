from .class_extractor import ClassExtractor


class PushDownFieldDetector:
    def __init__(self, project_path):
        self.project_path = project_path
        self.class_extractor = ClassExtractor(project_path)

    def extract_project_structure(self):
        self.class_extractor.extract_all_classes()
