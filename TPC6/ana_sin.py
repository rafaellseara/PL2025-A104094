from ana_lex import lexer

def tokenize(expression):
    lexer.input(expression)
    tokens = []
    
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append((token.type, token.value))
    
    return tokens

def parse_expression(tokens):
    node, tokens = parse_term(tokens)
    
    while tokens and tokens[0][0] in ('PLUS', 'MINUS'):
        operator, _ = tokens.pop(0)
        right_node, tokens = parse_term(tokens)
        node = [operator, node, right_node]
    
    return node, tokens

def parse_term(tokens):
    node, tokens = parse_factor(tokens)
    
    while tokens and tokens[0][0] in ('TIMES', 'DIVIDE'):
        operator, _ = tokens.pop(0)
        right_node, tokens = parse_factor(tokens)
        node = [operator, node, right_node]
    
    return node, tokens

def parse_factor(tokens):
    if not tokens or tokens[0][0] != 'NUM':
        raise ValueError("Expected a number")
    
    value = tokens.pop(0)[1]
    return value, tokens
