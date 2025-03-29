def calc(ast):
    if isinstance(ast, int):
        return ast
    if isinstance(ast, list):
        op, esq, dir = ast
        ve = calc(esq)
        vd = calc(dir)
        if op == 'PLUS':
            return ve + vd
        elif op == 'MINUS':
            return ve - vd
        elif op == 'TIMES':
            return ve * vd
        elif op == 'DIVIDE':
            return ve / vd
    raise ValueError("Expressão inválida")