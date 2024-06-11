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
        4,0,11,56,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,1,0,1,0,1,1,1,1,
        1,2,4,2,31,8,2,11,2,12,2,32,1,3,1,3,1,4,1,4,1,5,1,5,1,5,1,6,1,6,
        1,7,1,7,1,8,1,8,1,9,1,9,1,10,4,10,51,8,10,11,10,12,10,52,1,10,1,
        10,0,0,11,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,1,
        0,3,1,0,65,90,1,0,97,122,3,0,9,10,13,13,32,32,57,0,1,1,0,0,0,0,3,
        1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,
        0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,1,23,1,
        0,0,0,3,27,1,0,0,0,5,30,1,0,0,0,7,34,1,0,0,0,9,36,1,0,0,0,11,38,
        1,0,0,0,13,41,1,0,0,0,15,43,1,0,0,0,17,45,1,0,0,0,19,47,1,0,0,0,
        21,50,1,0,0,0,23,24,5,110,0,0,24,25,5,111,0,0,25,26,5,116,0,0,26,
        2,1,0,0,0,27,28,7,0,0,0,28,4,1,0,0,0,29,31,7,1,0,0,30,29,1,0,0,0,
        31,32,1,0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,6,1,0,0,0,34,35,7,0,
        0,0,35,8,1,0,0,0,36,37,7,1,0,0,37,10,1,0,0,0,38,39,5,58,0,0,39,40,
        5,45,0,0,40,12,1,0,0,0,41,42,5,46,0,0,42,14,1,0,0,0,43,44,5,44,0,
        0,44,16,1,0,0,0,45,46,5,40,0,0,46,18,1,0,0,0,47,48,5,41,0,0,48,20,
        1,0,0,0,49,51,7,2,0,0,50,49,1,0,0,0,51,52,1,0,0,0,52,50,1,0,0,0,
        52,53,1,0,0,0,53,54,1,0,0,0,54,55,6,10,0,0,55,22,1,0,0,0,3,0,32,
        52,1,6,0,0
    ]

class SODNLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    PREDICATE_VAR = 2
    PREDICATE_CONST = 3
    INDIVIDUAL_VAR = 4
    INDIVIDUAL_CONST = 5
    LEFT_ARROW = 6
    PERIOD = 7
    COMMA = 8
    LPAREN = 9
    RPAREN = 10
    WS = 11

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'not'", "':-'", "'.'", "','", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "PREDICATE_VAR", "PREDICATE_CONST", "INDIVIDUAL_VAR", "INDIVIDUAL_CONST", 
            "LEFT_ARROW", "PERIOD", "COMMA", "LPAREN", "RPAREN", "WS" ]

    ruleNames = [ "T__0", "PREDICATE_VAR", "PREDICATE_CONST", "INDIVIDUAL_VAR", 
                  "INDIVIDUAL_CONST", "LEFT_ARROW", "PERIOD", "COMMA", "LPAREN", 
                  "RPAREN", "WS" ]

    grammarFileName = "SODN.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


