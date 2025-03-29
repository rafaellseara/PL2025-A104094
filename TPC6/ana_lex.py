import ply.lex as lex

tokens = ['NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE']

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()