from ply import lex, yacc

import json

var = {}

#RESERVED TOKENS

reserved = {

    'print'  : 'PRINT',

    'if'     : 'IF',

}

literals = [' ']

#TOKENS

tokens = [

    'NUMBER',

    'PLUS',

    'MINUS',

    'TIMES',
    
    'EXPONENT',

    'DIVIDE',

    'LPAREN',

    'RPAREN',

    'LBRACE',

    'RBRACE',

    'QUESTIONMARK',

    'SINGLEQUOTE',

    'DOUBLEQUOTE',

    'ALPHABET',

    'COMMENT',

    'EQUALS',

    'IF_EQUALS',

] + list(reserved.values())

#TOKEN SYMBOLS

t_PLUS                  = r'\+'

t_MINUS                = r'-'

t_TIMES                = r'\*'

t_EXPONENT             = r'\^'

t_DIVIDE                = r'/'

t_LPAREN               = r'\('

t_RPAREN               = r'\)'

t_LBRACE               = r'\{'

t_RBRACE               = r'\}'

t_QUESTIONMARK      = r'\?'

t_ignore_COMMENT     = r'\#.*'

t_SINGLEQUOTE         = r"\'"

t_DOUBLEQUOTE        = r'\"'

t_EQUALS               = r'\='

t_IF_EQUALS            = r'\=='

#METHODS

def t_EXIT(t):

    r'exit()'

    print("Quitting program...")

    quit()

    return t

def t_PRINT(t):

    r'print'

    print(t.value.replace("print", "").replace("/t", "    "))

def t_ALPHABET(t):

    r'[a-zA-Z_][a-zA-Z_0-9]*'

    if t.value in var:

        t.value = var[str(t.value)]

    return t

def t_NUMBER(t):

    r'\d+'

    try:

        t.value = int(t.value)

    except ValueError:

        print(f"Integer value too large: {t.value}")

        t.value = 0

    return t

def t_newline(t):

    r'\n+'

    t.lexer.lineno += len(t.value)

# Error handling rule

def t_error(t):

    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

    t.lexer.skip(1)


t_ignore = ' \t'

lexer = lex.lex()

# Parsing

def p_expression_arithmetic(t):

    """expression : expression PLUS expression

                  | expression MINUS expression

                  | expression TIMES expression

                  | expression DIVIDE expression
                  
                  | expression EXPONENT expression"""


    if t[2] == '+'  :
        if ((isinstance(t[1], int) and isinstance(t[3], int)) or (isinstance(t[1], str) and isinstance(t[3], str))):
            t[0] = t[1] + t[3]
        elif isinstance(t[1], str) and isinstance(t[3], int):
            t[0] = t[1] + str(t[3])

    elif t[2] == '-': t[0] = t[1] - t[3]

    elif t[2] == '*': t[0] = t[1] * t[3]

    elif t[2] == '/': t[0] = t[1] / t[3]
    
    elif t[2] == '^': t[0] = t[1] ** t[3]

def p_expression_advance(t):

    """expression : expression IF_EQUALS expression

                  | expression EQUALS expression"""



    if t[2] == "==":

        if t[1] == t[3]:

            t[0] = True

        else:

            t[0] = False

        return

    elif t[2] == "=":

        var[str(t[1])] = t[3]

        pass



def p_expression_if(t):

    """expression : IF expression LBRACE expression RBRACE"""

    t[0] = t[4]

def p_expression_parenthesis(t):

    """expression : LPAREN expression RPAREN"""

    t[0] = t[2]

def p_expression_brace(t):

    """expression : LBRACE expression RBRACE"""

    t[0] = t[2]

def p_expression_singlequote(t):

    """expression : SINGLEQUOTE expression ALPHABET expression SINGLEQUOTE"""

    t[0] = t[2]

def p_expression_doublequote(t):

    """expression : DOUBLEQUOTE expression DOUBLEQUOTE"""

    t[0] = t[2]

def p_expression_alphabet(t):

    """expression : ALPHABET"""

    t[0] = t[1]

def p_expression_number(t):

    """expression : NUMBER"""

    t[0] = t[1]

def p_error(t):

    if not t is None: # lexer error

        print("Parsing failed")

        print(f"Syntax Error: {t.value!r}")

parser = yacc.yacc()

if __name__ == "__main__":

    while True:

        inp = input("~ ")

        print(parser.parse(inp))
