class Container:
    def __init__(self):
        self.dict = {}

    def add_element(self, elm):
        self.dict[elm.get_identifier()] = elm

    def has_element(self, identifier):
        return identifier in self.dict

    def get_element_by_identifier(self, identifier):
        return self.dict.get(identifier)

    def remove_element_by_identifier(self, identifier):
        self.dict.pop(identifier)

    def element_list(self):
        for key, element in self.dict.items():
            yield element
