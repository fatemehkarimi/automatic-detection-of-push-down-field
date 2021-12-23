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

    def local_variable_list(self):
        yield from self.local_variable_container.element_list()

    def has_variable_in_scope(self, var):
        for param in self.parameter_container.element_list():
            if var.get_identifier() == param.get_identifier():
                return True
        for local_var in self.local_variable_container.element_list():
            if var.get_identifier() == local_var.get_identifier():
                return True
        return False