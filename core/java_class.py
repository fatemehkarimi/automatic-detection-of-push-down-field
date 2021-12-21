from utils.container import Container


class JavaClass:
    def __init__(self, identifier):
        self.identifier = identifier
        self.field_container = Container()

    def get_identifier(self):
        return self.identifier

    def add_parent(self, parent):
        pass

    def add_field(self, field):
        self.field_container.add_element(field)

    def field_list(self):
        yield from self.field_container.element_list()
