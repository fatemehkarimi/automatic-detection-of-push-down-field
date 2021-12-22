from utils.container import Container


class JavaMethod:
    def __init__(self, identifier):
        self.identifier = identifier
        self.parameter_container = Container()
        self.local_variable_container = Container()

    def get_identifier(self):
        return self.identifier

    def add_parameter(self, param):
        self.parameter_container.add_element(param)

    def add_local_variable(self, variable):
        self.local_variable_container.add_element(variable)

    def parameter_list(self):
        yield from self.parameter_container.element_list()