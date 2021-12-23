from gen.JavaParserLabeledListener import JavaParserLabeledListener
from gen.JavaParserLabeled import  JavaParserLabeled
from .java_method import JavaMethod
from .java_field import JavaField
from .parse_utils import get_primitive_type
from utils.container import Container


class FieldUsageListener(JavaParserLabeledListener):
    def __init__(self, class_container):
        self.class_container = class_container
        self.class_stack = []
        self.current_method = None
        self.used_variable_container = None
        self.var_referencing_field_container = None
        self.reset_method()

    def reset_method(self):
        self.current_method = None
        self.used_variable_container = Container()
        self.var_referencing_field_container = Container()

    def set_class_used_fields(self):
        j_class = self.class_stack[-1]
        for used_var in self.var_referencing_field_container.element_list():
            j_class.add_used_field(used_var)

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
        if not (self.current_method and self.class_stack):
            self.reset_method()
            return

        for used_var in self.used_variable_container.element_list():
            if not self.current_method.has_variable_in_scope(used_var):
                self.var_referencing_field_container.add_element(used_var)

        self.set_class_used_fields()
        self.reset_method()

    def enterConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        # we only care about class constructors
        if not self.class_stack:
            return
        self.current_method = JavaMethod(self.class_stack[-1].get_identifier())

    def exitConstructorDeclaration(self, ctx:JavaParserLabeled.ConstructorDeclarationContext):
        if not(self.current_method and self.class_stack):
            self.reset_method()
            return

        for used_var in self.used_variable_container.element_list():
            if not self.current_method.has_variable_in_scope(used_var):
                self.var_referencing_field_container.add_element(used_var)

        self.set_class_used_fields()
        self.reset_method()

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

    def enterLocalVariableDeclaration(self, ctx:JavaParserLabeled.LocalVariableDeclarationContext):
        if not self.current_method:
            return
        variable_type = None
        if ctx.typeType().primitiveType():
            variable_type = get_primitive_type(ctx.typeType().primitiveType())
        if ctx.typeType().classOrInterfaceType():
            for var_type in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                variable_type = var_type.getText()

        for var in ctx.variableDeclarators().variableDeclarator():
            j_field = JavaField(var.variableDeclaratorId().IDENTIFIER().getText())
            j_field.set_type(variable_type)
            self.current_method.add_local_variable(j_field)

    def enterExpression0(self, ctx:JavaParserLabeled.Expression0Context):
        if not self.current_method:
            return
        if not isinstance(ctx.primary(), JavaParserLabeled.Primary4Context):
            return
        used_var = JavaField(ctx.primary().IDENTIFIER().getText())
        self.used_variable_container.add_element(used_var)

    def enterExpression1(self, ctx:JavaParserLabeled.Expression1Context):
        if not self.current_method:
            return

        if not (isinstance(ctx.expression(), JavaParserLabeled.Expression0Context)
                and isinstance(ctx.expression().primary(), JavaParserLabeled.Primary1Context)):
            return

        if ctx.expression().primary().THIS() and ctx.IDENTIFIER():
            j_field = JavaField(ctx.IDENTIFIER().getText())
            self.var_referencing_field_container.add_element(j_field)

    # variables used in constructors
    def enterExpression21(self, ctx:JavaParserLabeled.Expression21Context):
        if not self.current_method:
            return
        if not (isinstance(ctx.expression(), JavaParserLabeled.Expression0Context)
                and isinstance(ctx.expression().primary(), JavaParserLabeled.Primary4Context)):
            return
        used_var = JavaField(ctx.primary().IDENTIFIER().getText())
        self.used_variable_container.add_element(used_var)

    # variables defined in catch statement
    def enterCatchClause(self, ctx:JavaParserLabeled.CatchClauseContext):
        if not self.current_method:
            return
        if ctx.IDENTIFIER():
            self.current_method.add_local_variable(JavaField(ctx.IDENTIFIER().getText()))

    # variables defined in for(.. : ..) structure
    def enterEnhancedForControl(self, ctx:JavaParserLabeled.EnhancedForControlContext):
        if not self.current_method:
            return
        variable_type = None
        if ctx.typeType().classOrInterfaceType():
            for var in ctx.typeType().classOrInterfaceType().IDENTIFIER():
                variable_type = var.getText()
        if ctx.typeType().primitiveType():
            variable_type = get_primitive_type(ctx.typeType().primitiveType())
        j_field = JavaField(ctx.variableDeclaratorId().IDENTIFIER().getText())
        j_field.set_type(variable_type)
        self.current_method.add_local_variable(j_field)
