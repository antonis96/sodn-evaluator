grammar SODN;

// Parser rules

program         : (rule | fact)+ ;

rule            : predicate_head LEFT_ARROW body_expr PERIOD ;

fact            : predicate_head PERIOD ;

predicate_head  : predicate LPAREN arg_list RPAREN 
                | predicate ;

body_expr       : literal (COMMA literal)* ;

literal         : 'not' atom
                | atom ;

atom            : predicate LPAREN arg_list RPAREN 
                | predicate ;

arg_list        : arg (COMMA arg)* ;

arg             : INDIVIDUAL_CONST 
                | NUMBER
                | variable 
                | predicate_const ;

predicate_const : PREDICATE_CONST ;

variable        : INDIVIDUAL_VAR 
                | PREDICATE_VAR ;

predicate       : PREDICATE_CONST 
                | PREDICATE_VAR ;

// Lexer rules

PREDICATE_VAR   : [A-Z] ;
PREDICATE_CONST : [a-z] [a-z0-9_]* ;
INDIVIDUAL_VAR  : [A-Z] ;
INDIVIDUAL_CONST: [a-z] ;
NUMBER          : [0-9]+ ;

LEFT_ARROW      : ':-' ;
PERIOD          : '.' ;
COMMA           : ',' ;
LPAREN          : '(' ;
RPAREN          : ')' ;

// Ignore whitespaces
WS              : [ \t\r\n]+ -> skip ;
