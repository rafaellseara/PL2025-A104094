import ply.lex as lex

# Lista de tokens
tokens = (
    'KEYWORD', 'VAR', 'URI', 'STRING', 'SYMBOL', 'NUMBER'
)

# Definição de tokens
reserved = {'select', 'where', 'LIMIT'}

symbols = {'{', '}', '.', ':'}

def t_KEYWORD(t):
    r'select|where|LIMIT'
    return t

def t_VAR(t):
    r'\?[a-zA-Z_]\w*'
    return t

def t_URI(t):
    r'[a-zA-Z]+:[a-zA-Z_]\w*'
    return t

def t_STRING(t):
    r'".*?"@\w{2}'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SYMBOL(t):
    r'[{}.:]'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(query):
    lexer.input(query)
    tokens_list = []
    while tok := lexer.token():
        tokens_list.append((tok.value, tok.type))
    return tokens_list

if __name__ == "__main__":
    query = """
    select ?nome ?desc where {
        ?s a dbo:MusicalArtist.
        ?s foaf:name "Chuck Berry"@en .
        ?w dbo:artist ?s.
        ?w foaf:name ?nome.
        ?w dbo:abstract ?desc
    } LIMIT 1000
    """
    for token in tokenize(query):
        print(token)
