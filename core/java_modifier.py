class JavaModifier:
    def __init__(self):
        self.PUBLIC = False
        self.PROTECTED = False
        self.PRIVATE = False
        self.FINAL = False
        self.STATIC = False

    def set_public_flag(self, flag):
        self.PUBLIC = flag

    def set_protected_flag(self, flag):
        self.PROTECTED = flag

    def set_private_flag(self, flag):
        self.FINAL = flag

    def set_final_flag(self, flag):
        self.FINAL = flag

    def set_static_flag(self, flag):
        self.STATIC = flag

    def is_public(self):
        return self.PUBLIC

    def is_protected(self):
        return self.PROTECTED

    def is_private(self):
        return self.PRIVATE

    def is_final(self):
        return self.FINAL

    def is_static(self):
        return self.STATIC
