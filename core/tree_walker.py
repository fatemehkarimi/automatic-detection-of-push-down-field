"""
Class TreeWalker
- this class is a general parse tree walker that uses the listener passed to the
  class to walk over the parse tree.
"""

from antlr4 import CommonTokenStream, ParseTreeWalker
from gen.JavaLexer import JavaLexer
from gen.JavaParserLabeled import JavaParserLabeled


class TreeWalker:
    def __init__(self, listener):
        self.listener = listener

    def walk(self, stream):
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParserLabeled(token_stream)
        parse_tree = parser.compilationUnit()
        walker = ParseTreeWalker()
        walker.walk(t=parse_tree, listener=self.listener)

    def get_listener(self):
        return self.listener
