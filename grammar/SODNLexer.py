# Generated from SODN.g4 by ANTLR 4.13.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,12,65,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,1,0,1,
        0,1,1,1,1,1,2,1,2,5,2,34,8,2,10,2,12,2,37,9,2,1,3,1,3,1,4,1,4,1,
        5,4,5,44,8,5,11,5,12,5,45,1,6,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,
        10,1,10,1,11,4,11,60,8,11,11,11,12,11,61,1,11,1,11,0,0,12,1,1,3,
        2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,1,0,5,1,0,65,
        90,1,0,97,122,3,0,48,57,95,95,97,122,1,0,48,57,3,0,9,10,13,13,32,
        32,67,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,
        0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,
        0,0,21,1,0,0,0,0,23,1,0,0,0,1,25,1,0,0,0,3,29,1,0,0,0,5,31,1,0,0,
        0,7,38,1,0,0,0,9,40,1,0,0,0,11,43,1,0,0,0,13,47,1,0,0,0,15,50,1,
        0,0,0,17,52,1,0,0,0,19,54,1,0,0,0,21,56,1,0,0,0,23,59,1,0,0,0,25,
        26,5,110,0,0,26,27,5,111,0,0,27,28,5,116,0,0,28,2,1,0,0,0,29,30,
        7,0,0,0,30,4,1,0,0,0,31,35,7,1,0,0,32,34,7,2,0,0,33,32,1,0,0,0,34,
        37,1,0,0,0,35,33,1,0,0,0,35,36,1,0,0,0,36,6,1,0,0,0,37,35,1,0,0,
        0,38,39,7,0,0,0,39,8,1,0,0,0,40,41,7,1,0,0,41,10,1,0,0,0,42,44,7,
        3,0,0,43,42,1,0,0,0,44,45,1,0,0,0,45,43,1,0,0,0,45,46,1,0,0,0,46,
        12,1,0,0,0,47,48,5,58,0,0,48,49,5,45,0,0,49,14,1,0,0,0,50,51,5,46,
        0,0,51,16,1,0,0,0,52,53,5,44,0,0,53,18,1,0,0,0,54,55,5,40,0,0,55,
        20,1,0,0,0,56,57,5,41,0,0,57,22,1,0,0,0,58,60,7,4,0,0,59,58,1,0,
        0,0,60,61,1,0,0,0,61,59,1,0,0,0,61,62,1,0,0,0,62,63,1,0,0,0,63,64,
        6,11,0,0,64,24,1,0,0,0,4,0,35,45,61,1,6,0,0
    ]

class SODNLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    PREDICATE_VAR = 2
    PREDICATE_CONST = 3
    INDIVIDUAL_VAR = 4
    INDIVIDUAL_CONST = 5
    NUMBER = 6
    LEFT_ARROW = 7
    PERIOD = 8
    COMMA = 9
    LPAREN = 10
    RPAREN = 11
    WS = 12

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'not'", "':-'", "'.'", "','", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "PREDICATE_VAR", "PREDICATE_CONST", "INDIVIDUAL_VAR", "INDIVIDUAL_CONST", 
            "NUMBER", "LEFT_ARROW", "PERIOD", "COMMA", "LPAREN", "RPAREN", 
            "WS" ]

    ruleNames = [ "T__0", "PREDICATE_VAR", "PREDICATE_CONST", "INDIVIDUAL_VAR", 
                  "INDIVIDUAL_CONST", "NUMBER", "LEFT_ARROW", "PERIOD", 
                  "COMMA", "LPAREN", "RPAREN", "WS" ]

    grammarFileName = "SODN.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


