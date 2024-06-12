import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from .visitors import *

class CustomErrorListener(ErrorListener):
    def __init__(self):
        super(CustomErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = f"Syntax error at line {line}, column {column}: {msg}"
        self.errors.append(error_message)
        raise ParsingException(error_message)

class ParsingException(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse(program_text):
    try:
        input_stream = FileStream(program_text)
    except FileNotFoundError:
        raise ParsingException(f"File not found: {program_text}")
    except Exception as e:
        raise ParsingException(f"Error reading file {program_text}: {str(e)}")

    lexer = SODNLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SODNParser(stream)

    # Add custom error listener
    error_listener = CustomErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    try:
        tree = parser.program()
    except Exception as e:
        raise ParsingException(f"Parsing failed: {str(e)}")

    predicate_collector = PredicateCollector()
    walker = ParseTreeWalker()
    try:
        walker.walk(predicate_collector, tree)
    except Exception as e:
        raise ParsingException(f"Error during predicate collection: {str(e)}")

    builder = SODNBuilder(predicate_collector.predicates)
    try:
        walker.walk(builder, tree)
    except Exception as e:
        raise ParsingException(f"Error during program building: {str(e)}")


    type_collector = TypeCollector(predicate_collector.predicates)
    try:
        for _ in range(0, 3):
            walker.walk(type_collector, tree)
            type_collector.update_types()
    except Exception as e:
        raise ParsingException(f"Error during type collection and update: {str(e)}")

    program = builder.program
    program.types = type_collector.types
    program.predicates = predicate_collector.predicates
    return program