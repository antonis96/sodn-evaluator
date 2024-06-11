# Generated from SODN.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .SODNParser import SODNParser
else:
    from SODNParser import SODNParser

# This class defines a complete listener for a parse tree produced by SODNParser.
class SODNListener(ParseTreeListener):

    # Enter a parse tree produced by SODNParser#program.
    def enterProgram(self, ctx:SODNParser.ProgramContext):
        pass

    # Exit a parse tree produced by SODNParser#program.
    def exitProgram(self, ctx:SODNParser.ProgramContext):
        pass


    # Enter a parse tree produced by SODNParser#rule.
    def enterRule(self, ctx:SODNParser.RuleContext):
        pass

    # Exit a parse tree produced by SODNParser#rule.
    def exitRule(self, ctx:SODNParser.RuleContext):
        pass


    # Enter a parse tree produced by SODNParser#fact.
    def enterFact(self, ctx:SODNParser.FactContext):
        pass

    # Exit a parse tree produced by SODNParser#fact.
    def exitFact(self, ctx:SODNParser.FactContext):
        pass


    # Enter a parse tree produced by SODNParser#predicate_head.
    def enterPredicate_head(self, ctx:SODNParser.Predicate_headContext):
        pass

    # Exit a parse tree produced by SODNParser#predicate_head.
    def exitPredicate_head(self, ctx:SODNParser.Predicate_headContext):
        pass


    # Enter a parse tree produced by SODNParser#body_expr.
    def enterBody_expr(self, ctx:SODNParser.Body_exprContext):
        pass

    # Exit a parse tree produced by SODNParser#body_expr.
    def exitBody_expr(self, ctx:SODNParser.Body_exprContext):
        pass


    # Enter a parse tree produced by SODNParser#literal.
    def enterLiteral(self, ctx:SODNParser.LiteralContext):
        pass

    # Exit a parse tree produced by SODNParser#literal.
    def exitLiteral(self, ctx:SODNParser.LiteralContext):
        pass


    # Enter a parse tree produced by SODNParser#atom.
    def enterAtom(self, ctx:SODNParser.AtomContext):
        pass

    # Exit a parse tree produced by SODNParser#atom.
    def exitAtom(self, ctx:SODNParser.AtomContext):
        pass


    # Enter a parse tree produced by SODNParser#arg_list.
    def enterArg_list(self, ctx:SODNParser.Arg_listContext):
        pass

    # Exit a parse tree produced by SODNParser#arg_list.
    def exitArg_list(self, ctx:SODNParser.Arg_listContext):
        pass


    # Enter a parse tree produced by SODNParser#arg.
    def enterArg(self, ctx:SODNParser.ArgContext):
        pass

    # Exit a parse tree produced by SODNParser#arg.
    def exitArg(self, ctx:SODNParser.ArgContext):
        pass


    # Enter a parse tree produced by SODNParser#predicate_const.
    def enterPredicate_const(self, ctx:SODNParser.Predicate_constContext):
        pass

    # Exit a parse tree produced by SODNParser#predicate_const.
    def exitPredicate_const(self, ctx:SODNParser.Predicate_constContext):
        pass


    # Enter a parse tree produced by SODNParser#variable.
    def enterVariable(self, ctx:SODNParser.VariableContext):
        pass

    # Exit a parse tree produced by SODNParser#variable.
    def exitVariable(self, ctx:SODNParser.VariableContext):
        pass


    # Enter a parse tree produced by SODNParser#predicate.
    def enterPredicate(self, ctx:SODNParser.PredicateContext):
        pass

    # Exit a parse tree produced by SODNParser#predicate.
    def exitPredicate(self, ctx:SODNParser.PredicateContext):
        pass



del SODNParser