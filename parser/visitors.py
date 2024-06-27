from grammar.SODNLexer import SODNLexer
from grammar.SODNParser import SODNParser
from grammar.SODNListener import SODNListener
from components import *

class PredicateCollector(SODNListener):
    def __init__(self):
        self.predicates = set()

    def enterPredicate_head(self, ctx: SODNParser.Predicate_headContext):
        predicate = ctx.predicate().getText()
        self.predicates.add(predicate)

    def enterBody_expr(self, ctx: SODNParser.Body_exprContext):
        for literal_ctx in ctx.literal():
            atom_ctx = literal_ctx.atom()
            predicate = atom_ctx.predicate().getText()
            if predicate[0].islower():
                self.predicates.add(predicate)



class SODNBuilder(SODNListener):
    def __init__(self, predicates):
        self.program = Program()
        self.predicates = predicates
        self.current_rule = None
        self.current_fact = None
        self.errors = []

    def exitRule(self, ctx: SODNParser.RuleContext):
        if self.current_rule:
            self.program.add_rule(self.current_rule)
            self.current_rule = None

    def exitFact(self, ctx: SODNParser.FactContext):
        if self.current_fact:
            self.program.add_fact(self.current_fact)
            self.current_fact = None

    def enterPredicate_head(self, ctx: SODNParser.Predicate_headContext):
        predicate = ctx.predicate().getText()
        if ctx.arg_list():
            args = [self.build_argument(arg) for arg in ctx.arg_list().arg()]
            head = PredicateHead(predicate, args)
        else:
            head = PredicateHead(predicate)
        if self.current_rule is not None:
            self.current_rule.head = head
        if self.current_fact is not None:
            self.current_fact.head = head

    def enterBody_expr(self, ctx: SODNParser.Body_exprContext):
        literals = []
        for literal_ctx in ctx.literal():
            if literal_ctx.getText().startswith('not'):
                negated = True
                atom_ctx = literal_ctx.atom()
            else:
                negated = False
                atom_ctx = literal_ctx.atom()
            predicate = atom_ctx.predicate().getText()
            predicate_type = "predicate_variable" if predicate[0].isupper() else "predicate_const"

            if atom_ctx.arg_list():
                args = [self.build_argument(arg) for arg in atom_ctx.arg_list().arg()]
                atom = Atom(predicate, args, predicate_type)
            else:
                atom = Atom(predicate, predicate_type=predicate_type)
            literals.append(Literal(atom, negated))
        self.current_rule.body = literals

    def build_argument(self, arg_ctx):
        value = arg_ctx.getText()
        if value in self.predicates:
            arg_type = 'predicate_const'
        elif value.islower():
            arg_type = "data_const"
        else:
            arg_type = "variable"
        return Argument(value, arg_type)

    def enterRule(self, ctx: SODNParser.RuleContext):
        self.current_rule = Rule(None, [])

    def enterFact(self, ctx: SODNParser.FactContext):
        self.current_fact = Fact(None)

class TypeCollector(SODNListener):
    def __init__(self, predicates):
        self.types = {predicate: [None for _ in range(len(predicate))] for predicate in predicates}  # Initialize types as None
        self.variable_types = {}
        self.new_types = {predicate: None for predicate in predicates}

    def exitFact(self, ctx: SODNParser.FactContext):
        head = ctx.predicate_head()
        fact_predicate = head.predicate().getText()
        fact_args = [arg.getText() for arg in head.arg_list().arg()]
        fact_type = ['i' for _ in fact_args]

        if self.new_types[fact_predicate] is None:
            self.new_types[fact_predicate] = fact_type

    def exitRule(self, ctx: SODNParser.RuleContext):
        head = ctx.predicate_head()
        body = ctx.body_expr()

        head_predicate = head.predicate().getText()
        if head.arg_list() is None:
            head_type = 'o'
        else:
            head_args = [arg.getText() for arg in head.arg_list().arg()]

            # Initialize type for the head predicate
            head_type = []

            # Deduce type for each argument in the head
            for arg in head.arg_list().arg():
                arg_name = arg.getText()
                arg_type = self.deduce_arg_type(arg_name, body)
                head_type.append(arg_type)

        
        self.new_types[head_predicate] = head_type


    def deduce_arg_type(self, arg_name, body):
        if arg_name.islower():  # Constant
            return 'i'
        else:  # Variable
            for literal in body.literal():
                atom = literal.atom()
                body_predicate = atom.predicate().getText()
                body_args = [arg.getText() for arg in atom.arg_list().arg()]
                if arg_name == body_predicate:  # Predicate variable case
                    return ['i' for _ in body_args]
                if arg_name in body_args:  # Argument appears in the body
                    if body_predicate[0].isupper():
                        return 'i'
                    arg_index = body_args.index(arg_name)
                    if self.types[body_predicate] == [None]:
                        return None  # Defer type assignment
                    else:
                        print(self.types[body_predicate])
                        return self.types[body_predicate][arg_index]
            return None  # Defer type assignment

    def update_variable_type(self, var, var_type):
        if var not in self.variable_types:
            self.variable_types[var] = var_type

    def is_stable(self):
        for predicate in self.types:
            if self.types[predicate] != self.new_types[predicate]:
                return False
        return True

    def update_types(self):
        for predicate in self.types:
            self.types[predicate] = self.new_types[predicate]

    def get_types(self):
        return self.types

    def get_errors(self):
        return []
