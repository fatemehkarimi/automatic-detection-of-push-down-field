from gen.JavaParserLabeledListener import JavaParserLabeledListener
from gen.JavaParserLabeled import  JavaParserLabeled
from .java_method import JavaMethod
from .java_field import JavaField
from .parse_utils import get_primitive_type


class FieldUsageListener(JavaParserLabeledListener):
    def __init__(self, class_container):
        self.class_container = class_container
        self.class_stack = []
        self.current_method = None

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        j_class = self.class_container.get_element_by_identifier(ctx.IDENTIFIER().getText())
        if not j_class:
            raise Exception("class does not found in field usage extractor. this should not happen")
        self.class_stack.append(j_class)

    def exitClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        self.class_stack.pop()

    def enterMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        self.current_method = JavaMethod(ctx.IDENTIFIER().getText())

    def exitMethodDeclaration(self, ctx:JavaParserLabeled.MethodDeclarationContext):
        self.current_method = None

    def enterFormalParameter(self, ctx:JavaParserLabeled.FormalParameterContext):
        if not self.current_method:
            return

        j_field = JavaField(ctx.variableDeclaratorId().IDENTIFIER().getText())
        if ctx.typeType().classOrInterfaceType():
            for param_type in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                j_field.set_type(param_type.getText())

        if ctx.typeType().primitiveType():
            j_field.set_type(get_primitive_type(ctx.typeType().primitiveType()))
        self.current_method.add_parameter(j_field)
