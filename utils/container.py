class Container:
    def __init__(self):
        self.dict = {}

    def add_element(self, elm):
        self.dict[elm.get_name()] = elm

    def has_element(self, name):
        return name in self.dict

    def get_element_by_name(self, name):
        return self.dict.get(name)

    def remove_element_by_name(self, name):
        self.dict.pop(name)
