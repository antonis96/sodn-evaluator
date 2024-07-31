# Generated from SODN.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,12,88,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,4,0,27,8,0,
        11,0,12,0,28,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,
        1,3,3,3,45,8,3,1,4,1,4,1,4,5,4,50,8,4,10,4,12,4,53,9,4,1,5,1,5,1,
        5,3,5,58,8,5,1,6,1,6,1,6,1,6,1,6,1,6,3,6,66,8,6,1,7,1,7,1,7,5,7,
        71,8,7,10,7,12,7,74,9,7,1,8,1,8,1,8,1,8,3,8,80,8,8,1,9,1,9,1,10,
        1,10,1,11,1,11,1,11,0,0,12,0,2,4,6,8,10,12,14,16,18,20,22,0,2,2,
        0,2,2,4,4,1,0,2,3,85,0,26,1,0,0,0,2,30,1,0,0,0,4,35,1,0,0,0,6,44,
        1,0,0,0,8,46,1,0,0,0,10,57,1,0,0,0,12,65,1,0,0,0,14,67,1,0,0,0,16,
        79,1,0,0,0,18,81,1,0,0,0,20,83,1,0,0,0,22,85,1,0,0,0,24,27,3,2,1,
        0,25,27,3,4,2,0,26,24,1,0,0,0,26,25,1,0,0,0,27,28,1,0,0,0,28,26,
        1,0,0,0,28,29,1,0,0,0,29,1,1,0,0,0,30,31,3,6,3,0,31,32,5,7,0,0,32,
        33,3,8,4,0,33,34,5,8,0,0,34,3,1,0,0,0,35,36,3,6,3,0,36,37,5,8,0,
        0,37,5,1,0,0,0,38,39,3,22,11,0,39,40,5,10,0,0,40,41,3,14,7,0,41,
        42,5,11,0,0,42,45,1,0,0,0,43,45,3,22,11,0,44,38,1,0,0,0,44,43,1,
        0,0,0,45,7,1,0,0,0,46,51,3,10,5,0,47,48,5,9,0,0,48,50,3,10,5,0,49,
        47,1,0,0,0,50,53,1,0,0,0,51,49,1,0,0,0,51,52,1,0,0,0,52,9,1,0,0,
        0,53,51,1,0,0,0,54,55,5,1,0,0,55,58,3,12,6,0,56,58,3,12,6,0,57,54,
        1,0,0,0,57,56,1,0,0,0,58,11,1,0,0,0,59,60,3,22,11,0,60,61,5,10,0,
        0,61,62,3,14,7,0,62,63,5,11,0,0,63,66,1,0,0,0,64,66,3,22,11,0,65,
        59,1,0,0,0,65,64,1,0,0,0,66,13,1,0,0,0,67,72,3,16,8,0,68,69,5,9,
        0,0,69,71,3,16,8,0,70,68,1,0,0,0,71,74,1,0,0,0,72,70,1,0,0,0,72,
        73,1,0,0,0,73,15,1,0,0,0,74,72,1,0,0,0,75,80,5,5,0,0,76,80,5,6,0,
        0,77,80,3,20,10,0,78,80,3,18,9,0,79,75,1,0,0,0,79,76,1,0,0,0,79,
        77,1,0,0,0,79,78,1,0,0,0,80,17,1,0,0,0,81,82,5,3,0,0,82,19,1,0,0,
        0,83,84,7,0,0,0,84,21,1,0,0,0,85,86,7,1,0,0,86,23,1,0,0,0,8,26,28,
        44,51,57,65,72,79
    ]

class SODNParser ( Parser ):

    grammarFileName = "SODN.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'not'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "':-'", "'.'", "','", "'('", 
                     "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "PREDICATE_VAR", "PREDICATE_CONST", 
                      "INDIVIDUAL_VAR", "INDIVIDUAL_CONST", "NUMBER", "LEFT_ARROW", 
                      "PERIOD", "COMMA", "LPAREN", "RPAREN", "WS" ]

    RULE_program = 0
    RULE_rule = 1
    RULE_fact = 2
    RULE_predicate_head = 3
    RULE_body_expr = 4
    RULE_literal = 5
    RULE_atom = 6
    RULE_arg_list = 7
    RULE_arg = 8
    RULE_predicate_const = 9
    RULE_variable = 10
    RULE_predicate = 11

    ruleNames =  [ "program", "rule", "fact", "predicate_head", "body_expr", 
                   "literal", "atom", "arg_list", "arg", "predicate_const", 
                   "variable", "predicate" ]

    EOF = Token.EOF
    T__0=1
    PREDICATE_VAR=2
    PREDICATE_CONST=3
    INDIVIDUAL_VAR=4
    INDIVIDUAL_CONST=5
    NUMBER=6
    LEFT_ARROW=7
    PERIOD=8
    COMMA=9
    LPAREN=10
    RPAREN=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rule_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SODNParser.RuleContext)
            else:
                return self.getTypedRuleContext(SODNParser.RuleContext,i)


        def fact(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SODNParser.FactContext)
            else:
                return self.getTypedRuleContext(SODNParser.FactContext,i)


        def getRuleIndex(self):
            return SODNParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = SODNParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 24
                    self.rule_()
                    pass

                elif la_ == 2:
                    self.state = 25
                    self.fact()
                    pass


                self.state = 28 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==2 or _la==3):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicate_head(self):
            return self.getTypedRuleContext(SODNParser.Predicate_headContext,0)


        def LEFT_ARROW(self):
            return self.getToken(SODNParser.LEFT_ARROW, 0)

        def body_expr(self):
            return self.getTypedRuleContext(SODNParser.Body_exprContext,0)


        def PERIOD(self):
            return self.getToken(SODNParser.PERIOD, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_rule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRule" ):
                listener.enterRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRule" ):
                listener.exitRule(self)




    def rule_(self):

        localctx = SODNParser.RuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_rule)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.predicate_head()
            self.state = 31
            self.match(SODNParser.LEFT_ARROW)
            self.state = 32
            self.body_expr()
            self.state = 33
            self.match(SODNParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicate_head(self):
            return self.getTypedRuleContext(SODNParser.Predicate_headContext,0)


        def PERIOD(self):
            return self.getToken(SODNParser.PERIOD, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_fact

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFact" ):
                listener.enterFact(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFact" ):
                listener.exitFact(self)




    def fact(self):

        localctx = SODNParser.FactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_fact)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.predicate_head()
            self.state = 36
            self.match(SODNParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Predicate_headContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicate(self):
            return self.getTypedRuleContext(SODNParser.PredicateContext,0)


        def LPAREN(self):
            return self.getToken(SODNParser.LPAREN, 0)

        def arg_list(self):
            return self.getTypedRuleContext(SODNParser.Arg_listContext,0)


        def RPAREN(self):
            return self.getToken(SODNParser.RPAREN, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_predicate_head

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate_head" ):
                listener.enterPredicate_head(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate_head" ):
                listener.exitPredicate_head(self)




    def predicate_head(self):

        localctx = SODNParser.Predicate_headContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_predicate_head)
        try:
            self.state = 44
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 38
                self.predicate()
                self.state = 39
                self.match(SODNParser.LPAREN)
                self.state = 40
                self.arg_list()
                self.state = 41
                self.match(SODNParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.predicate()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Body_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SODNParser.LiteralContext)
            else:
                return self.getTypedRuleContext(SODNParser.LiteralContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SODNParser.COMMA)
            else:
                return self.getToken(SODNParser.COMMA, i)

        def getRuleIndex(self):
            return SODNParser.RULE_body_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBody_expr" ):
                listener.enterBody_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBody_expr" ):
                listener.exitBody_expr(self)




    def body_expr(self):

        localctx = SODNParser.Body_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_body_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.literal()
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9:
                self.state = 47
                self.match(SODNParser.COMMA)
                self.state = 48
                self.literal()
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(SODNParser.AtomContext,0)


        def getRuleIndex(self):
            return SODNParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)




    def literal(self):

        localctx = SODNParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_literal)
        try:
            self.state = 57
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.match(SODNParser.T__0)
                self.state = 55
                self.atom()
                pass
            elif token in [2, 3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self.atom()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def predicate(self):
            return self.getTypedRuleContext(SODNParser.PredicateContext,0)


        def LPAREN(self):
            return self.getToken(SODNParser.LPAREN, 0)

        def arg_list(self):
            return self.getTypedRuleContext(SODNParser.Arg_listContext,0)


        def RPAREN(self):
            return self.getToken(SODNParser.RPAREN, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)




    def atom(self):

        localctx = SODNParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_atom)
        try:
            self.state = 65
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.predicate()
                self.state = 60
                self.match(SODNParser.LPAREN)
                self.state = 61
                self.arg_list()
                self.state = 62
                self.match(SODNParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 64
                self.predicate()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Arg_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SODNParser.ArgContext)
            else:
                return self.getTypedRuleContext(SODNParser.ArgContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SODNParser.COMMA)
            else:
                return self.getToken(SODNParser.COMMA, i)

        def getRuleIndex(self):
            return SODNParser.RULE_arg_list

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArg_list" ):
                listener.enterArg_list(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArg_list" ):
                listener.exitArg_list(self)




    def arg_list(self):

        localctx = SODNParser.Arg_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_arg_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.arg()
            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9:
                self.state = 68
                self.match(SODNParser.COMMA)
                self.state = 69
                self.arg()
                self.state = 74
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INDIVIDUAL_CONST(self):
            return self.getToken(SODNParser.INDIVIDUAL_CONST, 0)

        def NUMBER(self):
            return self.getToken(SODNParser.NUMBER, 0)

        def variable(self):
            return self.getTypedRuleContext(SODNParser.VariableContext,0)


        def predicate_const(self):
            return self.getTypedRuleContext(SODNParser.Predicate_constContext,0)


        def getRuleIndex(self):
            return SODNParser.RULE_arg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArg" ):
                listener.enterArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArg" ):
                listener.exitArg(self)




    def arg(self):

        localctx = SODNParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_arg)
        try:
            self.state = 79
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                self.enterOuterAlt(localctx, 1)
                self.state = 75
                self.match(SODNParser.INDIVIDUAL_CONST)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 76
                self.match(SODNParser.NUMBER)
                pass
            elif token in [2, 4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 77
                self.variable()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 4)
                self.state = 78
                self.predicate_const()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Predicate_constContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PREDICATE_CONST(self):
            return self.getToken(SODNParser.PREDICATE_CONST, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_predicate_const

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate_const" ):
                listener.enterPredicate_const(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate_const" ):
                listener.exitPredicate_const(self)




    def predicate_const(self):

        localctx = SODNParser.Predicate_constContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_predicate_const)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(SODNParser.PREDICATE_CONST)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INDIVIDUAL_VAR(self):
            return self.getToken(SODNParser.INDIVIDUAL_VAR, 0)

        def PREDICATE_VAR(self):
            return self.getToken(SODNParser.PREDICATE_VAR, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)




    def variable(self):

        localctx = SODNParser.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_variable)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            _la = self._input.LA(1)
            if not(_la==2 or _la==4):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PredicateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PREDICATE_CONST(self):
            return self.getToken(SODNParser.PREDICATE_CONST, 0)

        def PREDICATE_VAR(self):
            return self.getToken(SODNParser.PREDICATE_VAR, 0)

        def getRuleIndex(self):
            return SODNParser.RULE_predicate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPredicate" ):
                listener.enterPredicate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPredicate" ):
                listener.exitPredicate(self)




    def predicate(self):

        localctx = SODNParser.PredicateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_predicate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            _la = self._input.LA(1)
            if not(_la==2 or _la==3):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





