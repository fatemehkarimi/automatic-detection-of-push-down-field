from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
from .java_class import JavaClass
from utils.container import Container


class ClassExtractorListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_stack = []
        self.class_container = Container()

    def enterClassDeclaration(self, ctx:JavaParserLabeled.ClassDeclarationContext):
        j_class = JavaClass(ctx.IDENTIFIER().getText())
        self.class_stack.append(j_class)
        self.class_container.add_element(j_class)

        if ctx.EXTENDS():
            for parent in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                j_class.add_parent(parent.getText())

        if ctx.IMPLEMENTS():
            for interface in ctx.typeList().typeType():
                for parent in interface.classOrInterfaceType().IDENTIFIER():
                    j_class.add_parent(parent.getText())
