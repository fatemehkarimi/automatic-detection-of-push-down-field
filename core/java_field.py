class JavaField:
    def __init__(self, identifier):
        self.identifier = identifier
        self.modifier = None
        self.type = None

    def get_identifier(self):
        return self.identifier

    def set_modifier(self, modifier):
        self.modifier = modifier

    def get_modifier(self):
        return self.modifier

    def set_type(self, field_type):
        self.type = field_type

    def get_type(self):
        return self.type
