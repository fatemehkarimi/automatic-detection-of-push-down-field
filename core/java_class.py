from utils.container import Container


class JavaClass:
    def __init__(self, identifier):
        self.identifier = identifier
        self.parent_container = Container()
        self.children_container = Container()
        self.field_container = Container()
        self.used_field_container = Container()
        self.parent_identifiers = []

    def get_identifier(self):
        return self.identifier

    def add_parent_identifier(self, parent):
        self.parent_identifiers.append(parent)

    def add_parent(self, parent):
        self.parent_container.add_element(parent)

    def add_field(self, field):
        self.field_container.add_element(field)

    def add_used_field(self, field):
        self.used_field_container.add_element(field)

    def add_child(self, child):
        self.children_container.add_element(child)

    def get_used_field_container(self):
        return self.used_field_container

    def get_field_container(self):
        return self.field_container

    def field_list(self):
        yield from self.field_container.element_list()

    def used_field_list(self):
        yield from self.used_field_container.element_list()

    def parent_list(self):
        yield from self.parent_container.element_list()

    def children_list(self):
        yield from self.children_container.element_list()
