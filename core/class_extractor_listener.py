from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
from .java_class import JavaClass
from .java_modifier import JavaModifier
from .java_field import JavaField
from .parse_utils import get_primitive_type
from utils.container import Container


class ClassExtractorListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_stack = []
        self.modifier_stack = []
        self.class_container = Container()

    def get_class_container(self):
        return self.class_container

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        j_class = JavaClass(ctx.IDENTIFIER().getText())
        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                j_class.add_parent(parent.getText())

        if ctx.IMPLEMENTS():
            for interface in ctx.typeList().typeType():
                for parent in interface.classOrInterfaceType().IDENTIFIER():
                    j_class.add_parent(parent.getText())

        self.class_stack.append(j_class)
        self.class_container.add_element(j_class)

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.class_stack.pop()

    def enterClassBodyDeclaration2(self, ctx:JavaParserLabeled.ClassBodyDeclaration2Context):
        # We only care about field modifiers
        if not isinstance(ctx.memberDeclaration(), JavaParserLabeled.MemberDeclaration2Context):
            return

        field_modifier = JavaModifier()
        for m in ctx.modifier():
            if m.classOrInterfaceModifier():
                if m.classOrInterfaceModifier().PUBLIC():
                    field_modifier.set_public_flag(True)
                if m.classOrInterfaceModifier().PROTECTED():
                    field_modifier.set_protected_flag(True)
                if m.classOrInterfaceModifier().PRIVATE():
                    field_modifier.set_private_flag(True)
                if m.classOrInterfaceModifier().STATIC():
                    field_modifier.set_static_flag(True)
                if m.classOrInterfaceModifier().FINAL():
                    field_modifier.set_final_flag(True)
        self.modifier_stack.append(field_modifier)

    def enterFieldDeclaration(self, ctx:JavaParserLabeled.FieldDeclarationContext):
        if not self.class_stack:
            return

        if not self.modifier_stack:
            raise Exception("modifier stack is empty. this should not happen")

        field_identifier = ""
        for variable in ctx.variableDeclarators().variableDeclarator():
            field_identifier = variable.variableDeclaratorId().IDENTIFIER().getText()
        java_field = JavaField(field_identifier)

        field_modifier = self.modifier_stack[-1]
        self.modifier_stack.pop()
        java_field.set_modifier(field_modifier)

        field_type = ''
        if ctx.typeType().classOrInterfaceType():
            for class_or_interface in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                field_type = class_or_interface.getText()

        if ctx.typeType().primitiveType():
            field_type = get_primitive_type(ctx.typeType().primitiveType())
        java_field.set_type(field_type)

        j_class = self.class_stack[-1]
        j_class.add_field(java_field)
