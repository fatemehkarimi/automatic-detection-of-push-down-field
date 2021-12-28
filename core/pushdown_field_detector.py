from .field_usage_extractor import FieldUsageExtractor
from .class_extractor import ClassExtractor
from utils.container import Container


class PushDownFieldDetector:
    def __init__(self, project_path):
        self.project_path = project_path
        self.project_class_container = Container()
        self.project_usage_dic = {}

    def extract_project_classes(self):
        class_extractor = ClassExtractor(self.project_path)
        class_extractor.extract_all_classes()
        self.project_class_container = class_extractor.get_project_classes()

    def extract_field_usage(self):
        field_usage_extractor = FieldUsageExtractor(self.project_path, self.project_class_container)
        field_usage_extractor.extract_field_usage()

    def detect_project_push_down_positions(self):
        for j_class in self.project_class_container.element_list():
            class_usage_dic = {}
            j_class_non_private_fields = Container()
            for def_field in j_class.field_list():
                if not def_field.get_modifier().is_private():
                    j_class_non_private_fields.add_element(def_field)
                    class_usage_dic[def_field.get_identifier()] = []

            self.detect_class_push_down_positions(j_class, j_class_non_private_fields, class_usage_dic)
            self.project_usage_dic[j_class.get_identifier()] = class_usage_dic

    def detect_class_push_down_positions(self, j_class, def_fields_container, class_usage_dic):
        new_def_field_container = Container()
        for def_field in def_fields_container.element_list():
            if j_class.get_used_field_container().has_element(def_field.get_identifier()):
                class_usage_dic[def_field.get_identifier()].append(j_class)
            else:
                new_def_field_container.add_element(
                    def_fields_container.get_element_by_identifier(def_field.get_identifier()))

        for child_class in j_class.children_list():
            self.detect_class_push_down_positions(child_class, new_def_field_container, class_usage_dic)

    def print_report(self):
        project_needs_refactoring = False
        for j_class in self.project_usage_dic:
            class_needs_refactor = False
            var_dicts = {}
            for field, child_list in self.project_usage_dic[j_class].items():
                if child_list:
                    var_dicts[field] = []
                    for child_class in child_list:
                        if j_class != child_class.get_identifier():
                            class_needs_refactor = True
                            var_dicts[field].append(child_class.get_identifier())

            if class_needs_refactor:
                project_needs_refactoring = True
                print(f"--------------- class {j_class} ---------------")
                for var in var_dicts:
                    if var_dicts[var]:
                        print(f"move VAR {var} in class {j_class} to ", end="")
                        for child_class in var_dicts[var][:-1]:
                            print(child_class, end=", ")
                        print(var_dicts[var][-1], end='.\n')
                print("")
        if not project_needs_refactoring:
            print("no push down refactoring situation found. enjoy the day!")
